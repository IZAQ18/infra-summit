"""Bounded async tools with explicit recording and fail-closed replay.

Credentials belong in provider closures, never in tool payloads. Recording is
opt-in per tool: its sanitizer must return only safe, replayable output fields.
Trace events contain metadata only; raw inputs, outputs and exceptions stay out.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Awaitable, Callable

Payload = dict[str, Any]


class ReplayMiss(RuntimeError):
    pass


class ToolFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class Tool:
    name: str
    version: str
    call: Callable[[Payload], Awaitable[Payload]]
    validate: Callable[[Payload], Payload]
    sanitize: Callable[[Payload], Payload] | None = None
    retry_safe: bool = False


class Runtime:
    def __init__(self, cache: Path, mode: str = "live", timeout: float = 20,
                 retries: int = 0):
        if mode not in {"live", "record", "replay"}:
            raise ValueError("Unknown runtime mode")
        if timeout <= 0 or retries < 0:
            raise ValueError("Invalid runtime limits")
        self.cache, self.mode = cache, mode
        self.timeout, self.retries = timeout, retries
        self.tools: dict[str, Tool] = {}
        self.trace: list[Payload] = []

    @classmethod
    def from_env(cls, cache: Path) -> Runtime:
        return cls(cache, "replay" if os.getenv("REPLAY") == "1"
                   else os.getenv("RUNTIME_MODE", "live"))

    def register(self, tool: Tool) -> None:
        if tool.name in self.tools:
            raise ValueError("Duplicate tool")
        self.tools[tool.name] = tool

    async def run(self, name: str, payload: Payload) -> Payload:
        tool = self.tools[name]
        canonical = json.dumps([name, tool.version, payload], sort_keys=True,
                               allow_nan=False, separators=(",", ":"))
        key = hashlib.sha256(canonical.encode()).hexdigest()
        path = self.cache / (key + ".json")
        event = {"tool": name, "version": tool.version, "mode": self.mode}
        if self.mode == "replay":
            if not path.is_file():
                self.trace.append(event | {"status": "replay_miss"})
                raise ReplayMiss("No recording for this exact request and version")
            result = tool.validate(json.loads(path.read_text(encoding="utf-8")))
            self.trace.append(event | {"status": "replayed"})
            return result
        if self.mode == "record" and tool.sanitize is None:
            raise ValueError("Recording requires an explicit output sanitizer")
        attempts = 1 + (self.retries if tool.retry_safe else 0)
        for attempt in range(attempts):
            try:
                result = tool.validate(await asyncio.wait_for(
                    tool.call(payload), timeout=self.timeout))
            except (TimeoutError, ConnectionError):
                self.trace.append(event | {"status": "transient_failure", "attempt": attempt + 1})
                if attempt + 1 == attempts:
                    raise ToolFailure("Tool exhausted its allowed attempts") from None
                await asyncio.sleep(min(0.1 * 2 ** attempt, 1))
                continue
            except Exception:
                self.trace.append(event | {"status": "failed"})
                raise ToolFailure("Tool failed validation or execution") from None
            if self.mode == "record":
                safe = tool.validate(tool.sanitize(result))
                encoded = json.dumps(safe, sort_keys=True, allow_nan=False)
                self.cache.mkdir(parents=True, exist_ok=True)
                temp_path = None
                try:
                    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                            dir=self.cache, delete=False) as handle:
                        temp_path = Path(handle.name)
                        handle.write(encoded)
                    temp_path.replace(path)
                finally:
                    if temp_path is not None:
                        temp_path.unlink(missing_ok=True)
                result = safe
            self.trace.append(event | {"status": "ok", "attempt": attempt + 1})
            return result
        raise AssertionError("Unreachable")


async def route(runtime: Runtime, providers: list[str], request: Payload) -> Payload:
    """Try configured providers in order, including validation failures.

    No provider SDKs or paid defaults are configured. Replay misses never trigger
    live calls. Adapters must implement cancellable async I/O.
    """
    for provider in providers:
        try:
            return await runtime.run(provider, request)
        except (ToolFailure, ReplayMiss):
            continue
    raise ToolFailure("No configured provider returned a valid response")

import asyncio
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agent_core.runtime import Runtime, Tool, ToolFailure, ReplayMiss, route
from agent_core.evaluation import exact_match


def validate(value):
    if not isinstance(value, dict) or not isinstance(value.get("answer"), str):
        raise ValueError("Invalid response")
    return value


class RuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_record_replay_is_offline_and_versioned(self):
        async def live(payload):
            return {"answer": payload["question"], "api_key": "test-only-secret"}
        async def forbidden(payload):
            self.fail("Replay invoked the network")
        with tempfile.TemporaryDirectory() as folder:
            cache = Path(folder)
            record = Runtime(cache, "record")
            record.register(Tool("llm", "1", live, validate,
                                 lambda result: {"answer": result["answer"]}))
            self.assertEqual(await record.run("llm", {"question": "hello"}), {"answer": "hello"})
            self.assertNotIn("secret", next(cache.glob("*.json")).read_text())
            replay = Runtime(cache, "replay")
            replay.register(Tool("llm", "1", forbidden, validate))
            self.assertEqual(await replay.run("llm", {"question": "hello"}), {"answer": "hello"})
            with self.assertRaises(ReplayMiss):
                await replay.run("llm", {"question": "different"})
            newer = Runtime(cache, "replay")
            newer.register(Tool("llm", "2", forbidden, validate))
            with self.assertRaises(ReplayMiss):
                await newer.run("llm", {"question": "hello"})

    async def test_timeout_falls_back_without_exception_contents(self):
        async def slow(payload):
            await asyncio.sleep(1)
            return {"answer": "late"}
        async def good(payload):
            return {"answer": "fallback"}
        with tempfile.TemporaryDirectory() as folder:
            runtime = Runtime(Path(folder), timeout=0.01)
            runtime.register(Tool("first", "1", slow, validate))
            runtime.register(Tool("second", "1", good, validate))
            self.assertEqual(await route(runtime, ["first", "second"], {}), {"answer": "fallback"})

    async def test_mutating_tool_never_retried(self):
        calls = 0
        async def uncertain(payload):
            nonlocal calls
            calls += 1
            raise ConnectionError("private response content")
        with tempfile.TemporaryDirectory() as folder:
            runtime = Runtime(Path(folder), retries=3)
            runtime.register(Tool("submit", "1", uncertain, validate))
            with self.assertRaises(ToolFailure):
                await runtime.run("submit", {})
            self.assertEqual(calls, 1)
            self.assertNotIn("private", str(runtime.trace))

    async def test_retry_safe_tool_recovers(self):
        calls = 0
        async def transient(payload):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise ConnectionError()
            return {"answer": "recovered"}
        with tempfile.TemporaryDirectory() as folder:
            runtime = Runtime(Path(folder), retries=1)
            runtime.register(Tool("read", "1", transient, validate, retry_safe=True))
            self.assertEqual(await runtime.run("read", {}), {"answer": "recovered"})
            self.assertEqual(calls, 2)

    async def test_recording_requires_sanitizer(self):
        async def forbidden(payload):
            self.fail("Unsafe recording called provider")
        runtime = Runtime(Path("unused"), "record")
        runtime.register(Tool("unsafe", "1", forbidden, validate))
        with self.assertRaises(ValueError):
            await runtime.run("unsafe", {})

    def test_eval_denominator(self):
        self.assertEqual(exact_match([1, 2], [1, 0]), {"cases": 2, "correct": 1, "accuracy": 0.5})
        with self.assertRaises(ValueError):
            exact_match([], [])

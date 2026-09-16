"""One synthetic ACT forward/backward/optimizer step. Not task training."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import time

import torch
from policy_preflight import make_policy


def probe(device):
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA unavailable: check NVIDIA driver and CUDA PyTorch build. No CPU fallback claimed as GPU.")
    torch.set_num_threads(4)
    torch.manual_seed(7)
    policy = make_policy(device).train()
    batch = {"observation.state": torch.zeros(1, 18, device=device),
             "observation.images.front": torch.rand(1, 3, 128, 128, device=device),
             "observation.images.side": torch.rand(1, 3, 128, 128, device=device),
             "action": torch.zeros(1, 10, 12, device=device),
             "action_is_pad": torch.zeros(1, 10, dtype=torch.bool, device=device)}
    optimizer = torch.optim.AdamW(policy.parameters(), lr=1e-5)
    cuda_info = None
    if device == "cuda":
        props = torch.cuda.get_device_properties(0)
        cuda_info = {"name": props.name, "vram_bytes": props.total_memory,
                     "capability": list(torch.cuda.get_device_capability(0)),
                     "torch_cuda_version": torch.version.cuda}
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.synchronize()
    started = time.perf_counter()
    loss, losses = policy(batch)
    if not torch.isfinite(loss):
        raise RuntimeError("Nonfinite synthetic loss")
    loss.backward()
    gradients = [p.grad for p in policy.parameters() if p.grad is not None]
    if not gradients or not all(torch.isfinite(g).all().item() for g in gradients):
        raise RuntimeError("Missing or nonfinite gradients")
    optimizer.step()
    if device == "cuda":
        torch.cuda.synchronize()
    return {"kind": "SYNTHETIC_SINGLE_STEP_NOT_TASK_TRAINING", "utc": datetime.now(timezone.utc).isoformat(),
            "os": platform.platform(), "python": platform.python_version(), "torch": torch.__version__,
            "device": device, "cuda": cuda_info, "batch_size": 1, "image_size": [128, 128],
            "optimizer_steps": 1, "seconds": time.perf_counter() - started,
            "loss": loss.item(), "loss_components": losses, "finite_gradients": True,
            "peak_cuda_allocated_bytes": torch.cuda.max_memory_allocated() if device == "cuda" else None,
            "checkpoint_saved": False, "task_success": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cuda")
    parser.add_argument("--output", type=Path, default=Path("artifacts/training-preflight/report.json"))
    args = parser.parse_args()
    report = probe(args.device)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

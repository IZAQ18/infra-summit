"""ACT/OpenVINO runtime probe with RANDOM weights. Never executes robot actions."""
import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import time

import numpy as np
import torch
from PIL import Image
from lerobot.configs.types import FeatureType, PolicyFeature
from lerobot.policies.act.configuration_act import ACTConfig
from lerobot.policies.act.modeling_act import ACTPolicy


def make_policy(device="cpu"):
    config = ACTConfig(device=device, chunk_size=10, n_action_steps=1,
                       pretrained_backbone_weights=None,
                       input_features={"observation.state": PolicyFeature(FeatureType.STATE, (18,)),
                                       "observation.images.front": PolicyFeature(FeatureType.VISUAL, (3, 128, 128)),
                                       "observation.images.side": PolicyFeature(FeatureType.VISUAL, (3, 128, 128))},
                       output_features={"action": PolicyFeature(FeatureType.ACTION, (12,))})
    return ACTPolicy(config).to(device)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--images", type=Path, default=Path("artifacts/local-smoke-separated"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/policy-preflight"))
    parser.add_argument("--openvino", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(4)
    torch.manual_seed(7)
    policy = make_policy().eval()
    # Recorded simulator frames; identity-normalized tensors for a shape/runtime probe.
    # This is not a trained preprocessing pipeline or multimodal phase reasoning.
    batch = {"observation.state": torch.zeros(1, 18)}
    for camera in ("front", "side"):
        image = np.asarray(Image.open(args.images / f"initial-{camera}.png").convert("RGB").resize((128, 128)), dtype=np.float32) / 255
        batch[f"observation.images.{camera}"] = torch.from_numpy(image.transpose(2, 0, 1).copy()).unsqueeze(0)
    elapsed = []
    with torch.inference_mode():
        policy.predict_action_chunk(batch)  # one unmeasured warmup
        for _ in range(5):
            start = time.perf_counter()
            result = policy.predict_action_chunk(batch)
            elapsed.append((time.perf_counter() - start) * 1000)
    assert result.shape == (1, 10, 12) and torch.isfinite(result).all()
    report = {"kind": "RANDOM_WEIGHT_RUNTIME_PROBE_NOT_TASK_POLICY", "utc": datetime.now(timezone.utc).isoformat(),
              "os": platform.platform(), "python": platform.python_version(),
              "versions": {p: importlib.metadata.version(p) for p in ("torch", "torchvision", "lerobot", "openvino")},
              "parameters": sum(p.numel() for p in policy.parameters()), "cpu_threads": 4,
              "checkpoint": None, "seed": 7, "warmup": 1, "samples": 5,
              "state_shape": [1, 18], "camera_shapes": [[1, 3, 128, 128]] * 2,
              "output_shape": list(result.shape), "finite": True,
              "native_ms": elapsed, "task_success": None, "actions_executed": 0}
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    if args.openvino:
        import openvino as ov

        class Wrapper(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self.policy = policy

            def forward(self, state, front, side):
                return self.policy.predict_action_chunk({"observation.state": state,
                    "observation.images.front": front, "observation.images.side": side})

        inputs = tuple(batch[k] for k in ("observation.state", "observation.images.front", "observation.images.side"))
        converted = ov.convert_model(Wrapper().eval(), example_input=inputs)
        core = ov.Core()
        compiled = core.compile_model(converted, "CPU", {"INFERENCE_NUM_THREADS": 4, "INFERENCE_PRECISION_HINT": "f32"})
        arrays = [t.numpy() for t in inputs]
        compiled(arrays)  # one warmup
        ov_times = []
        for _ in range(5):
            start = time.perf_counter()
            ov_output = compiled(arrays)[0]
            ov_times.append((time.perf_counter() - start) * 1000)
        error = float(np.max(np.abs(ov_output - result.numpy())))
        # Tracing warnings limit this export to the declared input shapes. Check
        # changed values too, so agreement is not just one fixed input fixture.
        changed = (torch.full_like(inputs[0], .25), inputs[2].flip(-1), inputs[1].flip(-2))
        with torch.inference_mode():
            changed_native = Wrapper().eval()(*changed).numpy()
        changed_ov = compiled([t.numpy() for t in changed])[0]
        changed_error = float(np.max(np.abs(changed_native - changed_ov)))
        report["openvino"] = {"device": "CPU", "full_device_name": core.get_property("CPU", "FULL_DEVICE_NAME"),
                              "available_devices": core.available_devices, "precision_hint": "f32",
                              "milliseconds": ov_times, "max_abs_error": error,
                              "changed_input_max_abs_error": changed_error,
                              "changed_input_parity": bool(np.allclose(changed_native, changed_ov, atol=1e-4, rtol=1e-4)),
                              "allclose_atol_1e-4_rtol_1e-4": bool(np.allclose(ov_output, result.numpy(), atol=1e-4, rtol=1e-4))}
        (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
        if not report["openvino"]["allclose_atol_1e-4_rtol_1e-4"] or not report["openvino"]["changed_input_parity"]:
            raise RuntimeError("Native/OpenVINO parity failed")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

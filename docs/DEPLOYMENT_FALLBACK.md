# Deployment fallback — 16 September 2026

The later event-channel guidance provides an alternative to waiting for Core Ultra
cloud allocation. The original PDF requested Core Ultra Series 2/3; preserve that
history rather than silently changing the claim.

## What the track guidance actually says

In the authenticated **Intel online challenge track** Discord, AmitB stated on
15 September that development/training may use an i7+GPU machine, while the VLA/VLM
policy must execute on Intel XPUs. He explicitly permitted an i7-13700K CPU/iGPU
and OpenVINO optimization. [Direct message source](https://discord.com/channels/877056448956346408/1547614813977575586/1549440623805989046).

On 16 September he clarified that no remote Core Ultra systems were reserved for
this event; the generally available cloud has its own lead time.
[Access clarification](https://discord.com/channels/877056448956346408/1547614813977575586/1549715430086541343).

**Our interpretation:** the available i5-1245U is a reasonable Intel-XPU deployment
fallback under this general permission. That exact processor was not individually
approved in the message. Report its real name and capabilities; do not claim a
Core Ultra, NPU run, or equivalent performance. A random-weight runtime benchmark
does not satisfy the required learned task deployment.

Other useful clarifications:

- A drawer is optional; a shelf is allowed. [Source](https://discord.com/channels/877056448956346408/1547614813977575586/1549328870975606856).
- SO-101 remains the preferred/recommended common arm baseline. [Source](https://discord.com/channels/877056448956346408/1547614813977575586/1549411451859369995).
- Learned vision/language control must dominate; IK alone is not the intended
  solution. Scripted IK here is only a physics/teacher experiment. [Source](https://discord.com/channels/877056448956346408/1547614813977575586/1549440623805989046).
- The demonstration must cover ten scene variations, with reproducible code and
  assets. Screen recording is allowed. [Source](https://discord.com/channels/877056448956346408/1547614813977575586/1549442593891422299).

These clarifications do not establish a deadline extension or waive learned control,
task complexity, reproducibility, or honest measurement.

## Two-computer plan

1. **Current Intel laptop:** develop contact physics, collect verified demonstrations,
   then run the trained policy and measure actual end-to-end behavior with OpenVINO.
2. **Optional NVIDIA desktop:** verify CUDA, VRAM and an ACT optimizer step; only then
   run a bounded training pilot on genuine demonstrations. Export the same learned
   checkpoint back to the Intel laptop for evaluation.
3. **Intel cloud:** keep the existing request; allocation is useful if it arrives,
   but local work should no longer wait on it.

## Windows NVIDIA handoff

Clone this public repository on the NVIDIA computer. Existing caches and virtual
environments are machine-specific and must not be copied. Requires working Git,
an NVIDIA driver and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```powershell
git clone https://github.com/IZAQ18/infra-summit.git
cd infra-summit
./tools/setup_cuda.ps1
```

The setup uses a separate `.cache/cuda-venv`, Python 3.12, LeRobot 0.6.0 and official
CUDA 12.6 PyTorch 2.11.0 / torchvision 0.26.0 Windows wheels. Vendor indexes were
checked on 16 September: [torch](https://download.pytorch.org/whl/cu126/torch/),
[torchvision](https://download.pytorch.org/whl/cu126/torchvision/). No driver changes,
system-policy changes, paid services or automatic task training occur.

Output: `artifacts/training-preflight/report.json` with detected GPU, actual VRAM,
CUDA version, finite gradients, measured one-step time and peak allocated memory.
The default is CUDA and a missing GPU fails explicitly. One synthetic optimizer
step verifies the training runtime; it is not useful task learning or a checkpoint.

**Validation so far:** the same Python probe passed its explicit CPU path on the
i5-1245U. CUDA installation/execution and desktop capacity are still unverified.
If script execution is blocked by local policy, have the local agent run its
individual commands; do not lower machine security settings.

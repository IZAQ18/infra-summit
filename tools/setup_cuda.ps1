param([string]$Uv = 'uv')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
$env:UV_CACHE_DIR = Join-Path (Get-Location) '.cache/uv'
$null = Get-Command $Uv -ErrorAction Stop
$null = Get-Command nvidia-smi -ErrorAction Stop
& nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
if ($LASTEXITCODE -ne 0) { throw 'NVIDIA driver check failed' }
if (-not (Test-Path -LiteralPath '.cache/cuda-venv/Scripts/python.exe')) {
    & $Uv venv --python 3.12 .cache/cuda-venv
    if ($LASTEXITCODE -ne 0) { throw 'Python environment setup failed' }
}
# Official PyTorch CUDA 12.6 Windows wheels, verified in vendor index 2026-09-16.
& $Uv pip install --python .cache/cuda-venv/Scripts/python.exe --only-binary :all: torch==2.11.0+cu126 torchvision==0.26.0+cu126 --index https://download.pytorch.org/whl/cu126 --index-strategy unsafe-best-match
if ($LASTEXITCODE -ne 0) { throw 'CUDA PyTorch install failed' }
& $Uv pip install --python .cache/cuda-venv/Scripts/python.exe --only-binary :all: lerobot==0.6.0 numpy==2.2.6 pillow==12.3.0
if ($LASTEXITCODE -ne 0) { throw 'LeRobot runtime install failed' }
& .cache/cuda-venv/Scripts/python.exe tools/training_preflight.py --device cuda
if ($LASTEXITCODE -ne 0) { throw 'CUDA execution check failed; do not claim GPU readiness' }
& $Uv pip freeze --python .cache/cuda-venv/Scripts/python.exe | Set-Content -LiteralPath artifacts/training-preflight/installed-packages.txt -Encoding utf8
Write-Host 'Synthetic ACT step complete. This is runtime evidence, not a trained robot policy.'

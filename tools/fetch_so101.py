"""Download the pinned upstream SO101 model into the ignored local cache."""
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REVISION = "eecbe3e0a9ebb23e25ad7b2759b03884c6660903"
BASE = f"https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/{REVISION}/"
DEST = ROOT / ".cache" / "so101"
MANIFEST = ROOT / "simulation" / "upstream_manifest.json"


def download(path: str, local: str) -> dict:
    target = DEST / local
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        payload = target.read_bytes()
    else:
        request = urllib.request.Request(BASE + path, headers={"User-Agent": "LineProof-feasibility"})
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = response.read(40_000_001)
        if len(payload) > 40_000_000 or payload.startswith(b"version https://git-lfs"):
            raise RuntimeError(f"Unsupported asset size or LFS pointer: {path}")
        target.write_bytes(payload)
    return {"source": path, "local": local, "bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record-manifest", action="store_true", help="Maintainer-only initial hash capture")
    args = parser.parse_args()
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text())
        for entry in manifest["files"]:
            result = download(entry["source"], entry["local"])
            if result != entry:
                raise RuntimeError(f"Asset checksum mismatch: {entry['local']}")
        print(f"Verified {len(manifest['files'])} pinned assets")
        return
    if not args.record_manifest:
        raise RuntimeError("Missing committed upstream_manifest.json. Restore it from the repository.")
    entries = [download("Simulation/SO101/so101_new_calib.xml", "so101_new_calib.xml"),
               download("LICENSE", "LICENSE")]
    model = ET.parse(DEST / "so101_new_calib.xml")
    names = [mesh.attrib["file"] for mesh in model.findall("./asset/mesh")]
    if any(Path(name).name != name for name in names):
        raise RuntimeError("Unexpected upstream mesh path")
    with ThreadPoolExecutor(max_workers=4) as pool:
        entries.extend(pool.map(lambda name: download("Simulation/SO101/assets/" + name,
                                                      "assets/" + name), names))
    MANIFEST.parent.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps({"revision": REVISION, "files": entries}, indent=2) + "\n")
    print(f"Downloaded {len(entries)} files, {sum(e['bytes'] for e in entries)} bytes")


if __name__ == "__main__":
    main()

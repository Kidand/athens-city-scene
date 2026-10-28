"""Append the original camera and its actions, retaining existing geometry.

Usage: blender target.blend --python scripts/import_camera.py
The in-memory scene is changed, but not saved automatically. Save As explicitly
if you want to keep the imported camera. Existing cameras are not removed.
"""
import argparse
import json
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera-library", type=Path,
                        default=ROOT / "camera" / "original_camera.blend")
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    args = parser.parse_args(argv)
    if not args.camera_library.is_file():
        parser.error("Camera library not found.")
    metadata = json.loads((ROOT / "camera" / "original_camera_720.json").read_text(encoding="utf-8"))
    wanted_name = metadata["camera_name"]
    scene = bpy.context.scene
    existing = set(scene.objects)
    with bpy.data.libraries.load(str(args.camera_library.resolve()), link=False) as (source, target):
        if wanted_name not in source.objects:
            raise RuntimeError("The expected camera object is absent from the library.")
        target.objects = [wanted_name]
    camera = target.objects[0]
    if camera is None or camera.type != "CAMERA":
        raise RuntimeError("Camera append failed.")
    scene.collection.objects.link(camera)
    scene.camera = camera
    scene.frame_start = 1
    scene.frame_end = 720
    scene.render.fps = 24
    scene.render.fps_base = 1.0
    scene.frame_set(1)
    if not existing.issubset(set(scene.objects)):
        raise RuntimeError("An existing object was unexpectedly removed.")
    print(json.dumps({"imported_camera": camera.name,
                      "existing_objects_preserved": len(existing),
                      "frame_start": 1, "frame_end": 720,
                      "fps": 24, "saved": False}, ensure_ascii=True))


if __name__ == "__main__":
    main()

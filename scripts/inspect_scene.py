"""Inspect the open Blender scene without rendering or saving it.

Usage: blender -b scene/athens.blend --python scripts/inspect_scene.py
Optional script arguments follow --: --output report.json
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parent.parent


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-camera", type=Path,
                        default=ROOT / "camera" / "original_camera_720.json")
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return parser.parse_args(argv)


def public_path(raw):
    """Keep local/private absolute directories out of the JSON report."""
    resolved = Path(bpy.path.abspath(raw)).resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return "external/" + resolved.name


def camera_samples(scene):
    original_frame = scene.frame_current
    original_subframe = scene.frame_subframe
    rows = []
    try:
        for frame in range(scene.frame_start, scene.frame_end + 1):
            scene.frame_set(frame)
            camera = scene.camera
            data = camera.data
            rows.append([
                frame, [list(row) for row in camera.matrix_world],
                data.lens, data.sensor_width, data.sensor_height,
                data.shift_x, data.shift_y, data.clip_start, data.clip_end,
                data.type,
            ])
    finally:
        scene.frame_set(original_frame, subframe=original_subframe)
    return rows


def inspect(args):
    scene = bpy.context.scene
    missing = []
    for image in bpy.data.images:
        packed = bool(image.packed_file or len(image.packed_files))
        if image.source in {"FILE", "MOVIE", "SEQUENCE", "TILED"} and not packed:
            # Tiled and sequence assets are not used by this release. Report the
            # base path as-is if a different scene uses them.
            raw = image.filepath
            if not raw or not Path(bpy.path.abspath(raw)).is_file():
                missing.append({"image": image.name,
                                "path": public_path(raw) if raw else None})
    report = {
        "blender_version": bpy.app.version_string,
        "scene_file": Path(bpy.data.filepath).name or None,
        "counts": {
            "scene_objects": len(scene.objects),
            "scene_object_types": dict(sorted(Counter(o.type for o in scene.objects).items())),
            "meshes": len(bpy.data.meshes),
            "materials": len(bpy.data.materials),
            "images": len(bpy.data.images),
            "actions": len(bpy.data.actions),
        },
        "render": {
            "engine": scene.render.engine,
            "resolution_x": scene.render.resolution_x,
            "resolution_y": scene.render.resolution_y,
            "resolution_percentage": scene.render.resolution_percentage,
            "fps": scene.render.fps,
            "fps_base": scene.render.fps_base,
            "frame_start": scene.frame_start,
            "frame_end": scene.frame_end,
        },
        "missing_image_count": len(missing),
        "missing_images": missing,
        "camera": None,
    }
    if hasattr(scene, "cycles"):
        report["render"]["cycles_samples"] = scene.cycles.samples
    if scene.camera:
        rows = camera_samples(scene)
        digest = hashlib.sha256(json.dumps(rows).encode("utf-8")).hexdigest()
        camera = {
            "name": scene.camera.name,
            "sample_count": len(rows),
            "sample_sha256": digest,
            "hash_encoding": "UTF-8 json.dumps(samples), default separators",
            "lens_mm_min": min(row[2] for row in rows),
            "lens_mm_max": max(row[2] for row in rows),
        }
        if args.expected_camera.is_file():
            expected = json.loads(args.expected_camera.read_text(encoding="utf-8"))
            camera["expected_sample_sha256"] = expected["source_sample_sha256"]
            camera["matches_original_export"] = digest == expected["source_sample_sha256"]
        report["camera"] = camera
    return report


if __name__ == "__main__":
    args = arguments()
    text = json.dumps(inspect(args), indent=2, ensure_ascii=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text)

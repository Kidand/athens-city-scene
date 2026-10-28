"""Explicitly render ONE frame of the currently open Blender scene.

Usage: blender -b scene/athens.blend --python scripts/render_frame.py -- \
           --frame 345 --output renders/frame_0345.png
No animation render or scene save is performed. Existing outputs are refused.
"""
import argparse
import json
from pathlib import Path
import sys

import bpy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frame", type=int, default=345)
    parser.add_argument("--output", type=Path)
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    args = parser.parse_args(argv)
    scene = bpy.context.scene
    if not scene.camera:
        parser.error("The current scene has no active camera.")
    if not scene.frame_start <= args.frame <= scene.frame_end:
        parser.error("Frame must be inside the current scene's animation range.")
    output = args.output or Path("renders") / ("frame_%04d.png" % args.frame)
    if output.suffix.lower() != ".png":
        parser.error("Use an output filename ending in .png.")
    if output.exists():
        parser.error("Output already exists; choose a new filename.")
    output.parent.mkdir(parents=True, exist_ok=True)
    old_frame, old_subframe = scene.frame_current, scene.frame_subframe
    old_path = scene.render.filepath
    old_format = scene.render.image_settings.file_format
    old_extension = scene.render.use_file_extension
    try:
        scene.frame_set(args.frame)
        scene.render.filepath = str(output.resolve())
        scene.render.image_settings.file_format = "PNG"
        scene.render.use_file_extension = True
        # Keep the original engine, resolution, samples, denoising, camera,
        # lights, color management and all other render settings untouched.
        bpy.ops.render.render(write_still=True)
    finally:
        scene.render.filepath = old_path
        scene.render.image_settings.file_format = old_format
        scene.render.use_file_extension = old_extension
        scene.frame_set(old_frame, subframe=old_subframe)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("Render did not produce a nonempty output file.")
    print(json.dumps({"rendered_frame": args.frame,
                      "output_file": output.name,
                      "bytes": output.stat().st_size}))


if __name__ == "__main__":
    main()

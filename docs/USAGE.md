# Open, inspect and render

## Requirements

- Blender **4.3.2** is the verified version.
- Python 3 is needed only for the standalone manifest verifier.
- FFmpeg is needed only to recreate preview media from a completed movie.
- No add-on or Python package installation is required by the supplied scripts.

The editable source of truth is `scene/athens.blend`. Keep the release's
relative directory layout intact so external assets can resolve. Use the
complete scene/assets download described in the main README; a source-code
checkout that omits large files is not a complete scene.

Open `scene/athens.blend` in Blender. Press Numpad 0 for the active camera view
and use the timeline to inspect frames 1-720. The film is 30 seconds at 24 fps
and 1280 x 720. Save edits under a new filename to preserve the release copy.
This is an artistic reconstruction, not a claim that every building, material,
sculpture or historical period is archaeologically exact.

## Verify downloaded bytes

Run from the release root once the release manifest is present:

```sh
python scripts/verify_manifest.py manifest.json
```

The manifest uses `files` entries containing `path`, `bytes` and `sha256`.
The verifier checks every listed file, rejects unsafe paths and duplicates,
and exits with status 1 for missing files or mismatches. Unlisted files are
allowed; it does not delete, modify or execute any downloaded file.

## Inspect without rendering

```sh
blender --disable-autoexec -b scene/athens.blend --python scripts/inspect_scene.py
```

To save the JSON report instead of relying only on terminal output:

```sh
blender --disable-autoexec -b scene/athens.blend --python scripts/inspect_scene.py -- --output inspection.json
```

The report includes object/data counts, image-file availability, render timing
and settings, and a hash of the sampled camera. The script does not render or
save the scene. Private absolute asset directories are not included in its
JSON report. Blender's own startup messages can still show the file you open.

## Explicit single-frame render

Rendering can use several GB of memory and take substantial CPU time. It is
not part of inspection. When ready, explicitly request one frame:

```sh
blender --disable-autoexec -b scene/athens.blend --python scripts/render_frame.py -- --frame 345 --output renders/frame_0345.png
```

Frame 345 is the default if `--frame` is omitted. The script renders only that
frame to PNG, refuses to overwrite an existing output, and never invokes an
animation render. It keeps the scene's engine, samples, resolution, denoising,
lighting and color-management settings. It restores the frame and output
settings in memory afterwards and does not save the `.blend` file. A lower
sample count or another Blender version may change the rendered result; no
bit-identical rerender is promised.

## Reuse the original camera

See [CAMERA.md](CAMERA.md). The separate camera library preserves the original
animation rather than replacing it with a newly designed path.

## Recreate compact media

With the exact completed high-bitrate master available:

```sh
bash scripts/reproduce-preview-media.sh path/to/completed-master.mp4 media-new
```

Use a new output directory to avoid overwriting previews. This script performs
only FFmpeg decoding, scaling and encoding, not Blender rendering:

- MP4: full 30 seconds, 640 x 360, 24 fps, H.264, no audio.
- GIF: full 30 seconds, 360 x 202, 4 fps / 120 frames, looping, 80-color palette.
- Poster: a decoded frame at 12.5 seconds.
- Contact sheet: 12 chronological decoded views.

The previews are intentionally compressed. The master retains more detail;
the GIF also reduces temporal and color resolution. FFmpeg versions may
produce different encoded hashes from the same source.

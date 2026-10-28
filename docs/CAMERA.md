# Original 30-second camera

The camera in `scene/athens.blend` is the authoritative production camera.
It is also supplied separately for reuse:

- `camera/original_camera.blend`: an appendable Blender library containing the
  original camera object, camera data and animation actions. This is not a
  standalone renderable scene; append it rather than opening it as a project.
- `camera/original_camera_720.json`: one sampled camera state for each frame.
  It is an interchange/verification export, not a substitute for the original
  F-curve interpolation in the camera library.

## Timing and coordinates

| Setting | Value |
| --- | --- |
| Frame range | 1-720 inclusive |
| Playback | 24 fps, fps base 1.0 |
| Movie duration | 30.000 seconds |
| Coordinates | Blender world: X east, Y north, Z up; metres |
| Projection | Perspective |
| Animated focal length | 32-34 mm |
| Sensor | 36 x 24 mm |
| Clip planes | 1-60000 m |

JSON rows follow `row_fields` in the file: frame number, 4 x 4 world matrix,
then lens, sensor size, shifts, clipping planes and projection type. Matrices
are stored as rows, with translation in the final column. The first encoded
movie frame corresponds to Blender frame 1; no interpolated video frames were
added.

## Append to your own scene

From the release root, with Blender on your PATH:

```sh
blender --disable-autoexec your_scene.blend --python scripts/import_camera.py
```

The script appends the camera and its original actions, sets it as the active
camera, sets frames 1-720 at 24 fps, and moves to frame 1. Existing geometry,
lights and cameras are retained. It does not change your render engine,
resolution, materials or world, and it does not save your file. Use **Save As**
in Blender to preserve the resulting scene. Repeated imports create additional
cameras rather than replacing or deleting prior objects.

The camera follows the original world's scale and location. It will not
reframe an unrelated model automatically. The source project renders at
1280 x 720; choose that resolution yourself if you want the same aspect ratio
in another scene.

## Verify the trajectory

```sh
blender --disable-autoexec -b scene/athens.blend --python scripts/inspect_scene.py
```

The script samples every frame and reports `matches_original_export`. In
Blender 4.3.2, the original 720-row sample hash is:

```text
d59b1fd26029f7cf99f5e1df0e1c18c641e8341138831555ac422111f527b690
```

Hash input is UTF-8 `json.dumps(samples)` using Python's default separators,
with no trailing newline. It includes lens and sensor values as well as the
world matrix. Floating-point evaluation can differ across Blender versions;
a mismatch should be investigated rather than interpreted as proof of a
visible change. The standalone import was tested in Blender 4.3.2: all 720
samples matched, both original animation actions were retained, and the
factory scene's cube, light and camera remained present.

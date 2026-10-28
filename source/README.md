# Source and reproducibility boundary

`../scene/athens.blend` is the authoritative editable source for this release.
It contains the assembled geometry, materials, lighting and original animated
camera. Required external dependencies are distributed according to the main
README and the third-party license notices. Do not move the scene or assets
independently without updating their relative paths.

The portable utilities in `../scripts/` inspect the scene, render a single
frame on explicit request, append the original camera, verify release files,
and regenerate compact media from the completed movie. They are not a full
procedural rebuild of every modeling step. The release does not claim that
running a single generator recreates the entire project from an empty scene.

The camera is additionally preserved as an appendable Blender library and a
720-sample JSON export. See `../docs/CAMERA.md` and `../docs/USAGE.md`.

Third-party meshes, textures and other assets retain their own licenses and
attributions. Inclusion in this project does not imply original authorship of
those assets or of the ancient sculptures they depict. The scene is an
artistic reconstruction with documented limits, not an exact historical
survey.

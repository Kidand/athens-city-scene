# Third-party assets and source notices

This is a mixed-source artistic reconstruction. The project does not claim authorship of museum cast scans, third-party textures, trees, or elevation data. A licence for a tool such as Blender does not license the artwork. The included scene dependency groups have been checked against provider licence statements and source metadata. The notices below apply to the specified components; they are **not a blanket licence for the whole project** or a guarantee of rights in every jurisdiction.

## Sculpture geometry: SMK / National Gallery of Denmark

The following source records mark their downloadable cast scans `public_domain: true`, with [Public Domain Mark 1.0](https://creativecommons.org/publicdomain/mark/1.0/). PDM records public-domain status; it is not the CC0 dedication or a CC-BY licence. These are cast scans with losses/restorations, not newly scanned original ancient sculpture made by this project.

| Source | Use in this scene | Changes and limits |
| --- | --- | --- |
| [SMK KAS838 — cast after Caryatid C](https://open.smk.dk/en/artwork/image/KAS838) | Six Erechtheion supports, and an anatomical donor for inferred hands | Normalized and reduced; repeated/mirrored pose variants. One restored cast type after a Roman copy, **not six distinct original Greek figures**. |
| [SMK KAS2115 — East D, traditionally Dionysos](https://open.smk.dk/en/artwork/image/KAS2115) | Retained reclining figure core | Reduced and repositioned; missing extremities have separately authored inferred additions. |
| [SMK KAS2117 — East G, running woman](https://open.smk.dk/en/artwork/image/KAS2117) | Retained draped figure core | Reduced, scaled and repositioned; head/limbs reconstructed separately. Artemis/Hebe identification remains uncertain. |
| [SMK KAS2120 — East O, Selene horse head](https://open.smk.dk/en/artwork/image/KAS2120) | Four repeated corner-head proxies | Reduced and repositioned; four placements reuse **one** source head, not four authenticated originals. |

Credit: SMK / National Gallery of Denmark, collection and downloadable cast scans; KAS838 is associated with the museum's Scan the World collaboration. The ancient sculptors are not credited to this project. Other modeled anatomy, drapery, horses, accessories and concealed supports are interpretive additions, not museum-scan evidence. No endorsement by SMK is implied.

The University of Texas at Austin Department of Classics / Blanton Museum of Art [Dione–Aphrodite](https://battlecasts.la.utexas.edu/3D-model-entries/parthpedmerged-model.html) and [Hestia](https://battlecasts.la.utexas.edu/3D-model-entries/parthhestia-model.html) model pages provide CC0 models, but those optional candidates are **not incorporated in this production scene**. They are not bundled here. Unused noncommercial and authentication-restricted research candidates are also excluded.

## Surface textures, vegetation and sky

[Poly Haven's asset licence](https://polyhaven.com/license) and [ambientCG's asset licence](https://docs.ambientcg.com/license/) permit redistribution of their downloaded assets under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Credit is not required by CC0, but is retained here. Website text, logos, and unrelated reference pictures are not covered by this list.

| Asset | Author/provider |
| --- | --- |
| [Bark Brown 01](https://polyhaven.com/a/bark_brown_01) | Rob Tuytel / Poly Haven |
| [Clay Plaster](https://polyhaven.com/a/clay_plaster) | Amal Kumar / Poly Haven |
| [Clay Roof Tiles 02](https://polyhaven.com/a/clay_roof_tiles_02) | Amal Kumar / Poly Haven |
| [Dry Mud Field 001](https://polyhaven.com/a/dry_mud_field_001) | Rob Tuytel (photography), Rico Cilliers (processing) / Poly Haven |
| [Grass Medium 02](https://polyhaven.com/a/grass_medium_02) | Rico Cilliers / Poly Haven |
| [Kloofendal 43d Clear PureSky](https://polyhaven.com/a/kloofendal_43d_clear_puresky) | Greg Zaal / Poly Haven |
| [Marble Cliff 05](https://polyhaven.com/a/marble_cliff_05) | Amal Kumar / Poly Haven |
| [Marble Rock 02](https://polyhaven.com/a/marble_rock_02) | Amal Kumar / Poly Haven |
| [Old Stone Wall](https://polyhaven.com/a/old_stone_wall) | Charlotte Baglioni / Poly Haven |
| [Quarry Wall 02](https://polyhaven.com/a/quarry_wall_02) | Dimitrios Savva / Poly Haven |
| [Rock Boulder Dry](https://polyhaven.com/a/rock_boulder_dry) | Dimitrios Savva (photography), Rico Cilliers (processing) / Poly Haven |
| [Rocks Ground 06](https://polyhaven.com/a/rocks_ground_06) | Rob Tuytel / Poly Haven |
| [Rocky Trail 02](https://polyhaven.com/a/rocky_trail_02) | Amal Kumar / Poly Haven |
| [Rough Wood](https://polyhaven.com/a/rough_wood) | Rob Tuytel / Poly Haven |
| [Sandy Gravel](https://polyhaven.com/a/sandy_gravel) | Charlotte Baglioni / Poly Haven |
| [Shrub 02](https://polyhaven.com/a/shrub_02) | Rico Cilliers / Poly Haven |
| [White Plaster 02](https://polyhaven.com/a/white_plaster_02) | Rob Tuytel / Poly Haven |
| [White Stucco](https://polyhaven.com/a/white_stucco) | Amal Kumar / Poly Haven |
| [Marble025](https://ambientcg.com/a/Marble025) | Lennart Demes / ambientCG |
| [Mature olive tree](https://www.innerscene.com/tools/library/3d-parts/mature-olive-tree-bc261a43) | Innerscene, CC0 |
| [Columnar cypress tree](https://www.innerscene.com/tools/library/3d-parts/columnar-cypress-tree-46fad033) | Innerscene, CC0 |

The olive/cypress derivatives retain transformed source branches, with project-authored foliage refinements and material changes. Surface maps include recoloring, channel combinations, synthesized edge/detail variants and render-resolution downsampling. These modern materials and plants are visual analogues, not verified ancient material or botanical samples. The sky is a lighting source, not an Athens geographic panorama.

For a reproducible public release, the previous image-based groundcover colour mask is **not distributed**. The scene instead uses project-authored world-space noise and a colour ramp in four ground materials, and a zero-valued mask on the road material. See [`scripts/apply_procedural_groundcover.py`](../scripts/apply_procedural_groundcover.py). This material-only substitution changes neither geometry nor the camera. The preview media are encodings of the completed film made before this substitution, so local groundcover colour patches can differ from a new render.

## Adapted terrain

[Terrain Tiles](https://registry.opendata.aws/terrain-tiles/) — Mapzen, a Linux Foundation project — was accessed on 19 October 2026. The terrain uses Skadi tiles **N37E023** and **N38E023**. The provider's regional source-footprint data identifies SRTM, EU-DEM, GMTED2010 and ETOPO1 candidates; the exact source at every sample was not returned, so the notices are conservatively retained together. This is not labelled “CC0 terrain.” See [source-specific notices](https://github.com/tilezen/joerd/blob/master/docs/attribution.md).

- SRTM and GMTED2010 terrain data courtesy of the U.S. Geological Survey.
- Produced using Copernicus data and information funded by the European Union — EU-DEM layers.
- ETOPO1 terrain/bathymetry: DOC/NOAA/NESDIS/NCEI — National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce.

Modifications: crop, smoothing, conversion to a local true-north metre frame, adaptive triangular resampling, artistic vertical-datum shift and blending around modeled urban footprints. The final distant terrain includes later source-resampling corrections. It is an adapted visualization, **not an archaeological ground survey, navigation product or scientific elevation product**. No endorsement by the data providers is implied. [EU-DEM information](https://www.eea.europa.eu/en/datahub/datahubitem-view/d08852bc-7b5f-4835-a776-08362e2fbf4b).

## Geographic controls

Geographic positioning references include **[© OpenStreetMap contributors](https://www.openstreetmap.org/copyright)**. OpenStreetMap data is available under the [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/).

[`data/geographic-controls.json`](../data/geographic-controls.json) supplies the adapted scene control data for 14 civic objects, with their OpenStreetMap source links, under ODbL 1.0. Selection, transformation into project coordinates and artistic adjustments are identified as modifications.

This credit concerns geographic controls, not the authorship of the reconstructed architecture or sculpture. ODbL applies to OSM data and derivative databases; it does not automatically relicense unrelated code, textures, sculpture or the whole artwork. If exporting or redistributing OSM-derived coordinate/footprint datasets, keep the ODbL notices and satisfy its share-alike and machine-readable source requirements for the relevant dataset. Do not describe OSM-derived data as CC0. See the [OSMF attribution guidelines](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines).

## Reuse boundary

Third-party rights and attribution remain attached to their components. Do not remove these notices when redistributing the scene or its assets. Reference publications do not grant permission to redistribute their images. No museum reference photographs, source web pages, or proprietary/noncommercial model candidates are part of this package. Missing architectural and sculptural detail remains interpretive; this is a mixed-period reconstruction rather than a surveyed single-date model.

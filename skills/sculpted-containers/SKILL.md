---
name: sculpted-containers
description: Create sculptural vases and catchall bowls from editable radial profiles, flutes and twist, with STL/3MF models and exact-geometry previews. Use for this specific family of 3D printing models and variations.
---

# Sculpted Containers

Create actual model geometry, editable parameters and previews from the same mesh. The examples are starting briefs, not mandatory designs. Write a new JSON brief for the user's request; do not change SKILL.md to customize an object.

## Inputs and scope

Choose height, profile radii, radial wall/base thickness, flute depth/count and twist. Profiles are [height fraction, radius in millimeters] pairs, from 0 to 1. They define the silhouette, so the two examples can produce new shapes without source edits.

All dimensions are millimeters. Use example dimensions when unspecified and disclose them. If the request needs geometry outside these modes, explain the boundary and adapt the CAD source as a separate change with fresh mesh checks. Do not silently substitute a supported shape for an unsupported request.

## Run

Use a local Python environment. The dependency versions below were tested with Python 3.14. Install the bundled requirements with that environment's pip. FFmpeg with libx264 is optional for a six-second silent turntable video.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r <skill>/requirements.txt
.venv/bin/python <skill>/scripts/model_engine.py --config <brief.json> --out <new-directory>
# Add --video when a turntable MP4 is requested and FFmpeg is available.
```

The renderer rejects an existing output directory. Deliver `model.stl`, `model.3mf`, `parameters.json`, `checks.json`, `poster.png`, `preview.html` and `receipt.json`, plus `turntable.mp4` when requested. Keep the source script and parameters for reproducibility. Open preview.html locally to rotate, reveal height or save a PNG. WebGL is required; no CDN or network request is used. The HTML embeds the exact exported mesh positions, rounded to six decimals.

## Review

Confirm the reported dimensions match the brief. Inspect the poster, rotate the model and review the generated report. Geometry checks require finite coordinates, a closed/wound mesh, positive volume, nondegenerate triangles and one connected body. The generator uses Manifold for solid booleans and Trimesh for mesh checks. A turntable shows the actual exported geometry. A height reveal is only a geometry illustration, not a toolpath simulator.

Before printing, import STL as millimeters or use 3MF's explicit units in a slicer. Ask for the printer, nozzle and material only when preparing that stage. Inspect wall continuity, small features, supports, first-layer placement and build-volume fit with the actual profile. The bundled 3MF is single-material geometry, not a printer project. Do not generate printer-specific G-code or time/material claims without the appropriate profile.

State the actual status: mesh checked, slicer tested with a named profile, or physically printed. These examples are mesh checked only. Open-top single-wall vessels with closed bases. No drain holes or handles. Wall is radial separation, not measured minimum normal thickness. Bowls with expanding walls may need supports; review in your slicer.

## Worked examples

See [references/examples.md](references/examples.md) for two editable input briefs, exact invocations, and recorded outputs. Change the inputs through the user's brief. Preserve the distinction between an example mesh, a preview image and a physical print.

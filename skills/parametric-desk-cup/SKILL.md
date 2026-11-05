---
name: parametric-desk-cup
description: Create customizable fluted or twisted desk cups and decorative pots as editable parameters, STL and 3MF meshes, with an offline interactive 3D preview. Use for this family of 3D printing models and variations, not arbitrary sculpture or printer control.
---

# Parametric Desk Cup

Create an original open-top vessel with a closed base. The bundled generator uses Python 3's standard library. It produces real geometry and a preview of the exact exported mesh, without image generation, network services or paid APIs.

## Shape the brief

Translate the request into height, nominal body diameter, radial wall thickness, base thickness, flute count, flute depth, taper and twist. All distances are millimeters. Color affects only the preview. Use the supplied examples as starting points, not a fixed artistic result. Keep the editable JSON alongside the outputs so another person can reproduce or vary the design.

If dimensions are unspecified, use the pen-cup example and disclose the chosen dimensions. Printer information is not needed to create a model. It is needed before preparing printer-specific toolpaths or asserting bed fit. Ask for printer model, nozzle and material only when that stage is requested.

## Generate

Copy [assets/twist-cup.json](assets/twist-cup.json) or [assets/scalloped-pot.json](assets/scalloped-pot.json) to the working output area and edit the copy. Run:

```bash
python3 <skill>/scripts/make_vessel.py --config <brief.json> --out <new-output-directory>
```

The output directory must be new. The generator emits `model.stl`, `model.3mf`, `parameters.json`, `mesh.json`, `checks.json` and `preview.html`. The script itself is the reusable editable geometry source. STL coordinates must be imported as millimeters; 3MF explicitly records millimeters. The 3MF contains geometry, not a saved printer profile.

Open `preview.html` locally. Drag to rotate, change the reveal height, turn auto-rotation on or save a PNG. The preview is an offline Canvas rendering of the same indexed triangles as both mesh files. Height reveal is a geometry illustration, not a slicer toolpath or prediction of print success. Use screenshots or a screen recording when requested; do not substitute a generated illustration for geometry evidence.

## Verify and hand off

Review the mesh report and preview. The generator checks finite geometry, nonzero triangle areas, two oppositely directed faces per edge, one connected surface, positive enclosed volume and bounds. Its model family uses nested radial rings; do not generalize these checks into certification of arbitrary imported meshes. Radial wall thickness is not a measured minimum normal thickness. Extreme flute/twist combinations can produce thinner regions; inspect them in a slicer.

Give the user the model files, parameters and preview. Explain actual measured bounds, including the flute protrusions. State whether the file has only passed mesh checks, has been successfully sliced with a named profile, or has actually been printed. Never silently promote one status into another.

For a requested print-preparation stage, import into the user's slicer and confirm millimeter scale, upright base-on-bed orientation, wall continuity, overhang/support needs and bed fit. Use the actual printer, nozzle and material profile to generate G-code and its layer preview. Report estimated time/material only from that configured slicer. Keep printer-specific G-code separate from reusable meshes. A closed mesh does not establish liquid tightness or physical print quality.

## Adaptation boundary

The current generator makes one continuous cup, with no drain holes, handles, lettering or movable parts. Changes within its parameters need no source edits. For a new object family, create or adapt an appropriate CAD generator and revalidate the exported mesh; do not describe an unsupported prompt as completed. Practical next families include relief plaques and simple desktop organizers. Organic characters require a separate modeling and mesh-repair workflow.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.

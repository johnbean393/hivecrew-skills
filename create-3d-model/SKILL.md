---
name: reference-image-to-3d-model
description: Create simple textured 3D models as OBJ/MTL/texture files plus a dimensioned drawing from a single reference image or a generic object description. Use when Claude needs to: (1) analyze a reference image in Python to extract shape/profile coordinate points, (2) turn the image into a cylindrical or revolved texture when the object is approximately axisymmetric, (3) search the web for a generic reference image before modeling, or (4) return both a 3D model and an isometric drawing with dimensions.
---

# Reference Image To 3D Model

Build a textured OBJ model and a dimension sheet for objects that can be approximated as a surface of revolution: bottles, cans, cups, jars, thermoses, vases, candles, and similar front/side-view objects.

## Quick workflow

1. Decide whether the object is suitable.
   - Best fit: near-axisymmetric objects from a clean front or side image.
   - Poor fit: chairs, cars, shoes, animals, hands, or anything strongly asymmetric from a single view. Ask for more views if accuracy matters.
2. If a reference image exists, use `scripts/build_revolved_obj.py`.
3. If there is no reference image and the object is generic, first find one:
   - Use `web_search` with product-style queries.
   - Use `extract_info_from_webpage` to confirm the page really contains the object and any real dimensions.
   - Use `run_shell` with `curl -L` or `wget` to download the image.
4. Run the script to produce:
   - `name.obj`
   - `name.mtl` and optional texture PNG
   - `name_profile.csv`
   - `name_analysis.json`
   - `name_drawing.png` (dimensioned multi-view sheet)
5. Validate with `read_file` on the drawing PNG and inspect the analysis JSON.

## Generic reference-image search pattern

When no image is supplied, prefer a real reference image over inventing proportions.

Example queries:
- `site:target.com stainless steel water bottle front view white background`
- `site:walmart.com ceramic vase product photo front`
- `site:amazon.com soda can isolated white background`
- `"<object name>" product dimensions front view`

Example extraction questions:
- `Does this page show a clear front or side product image of the object?`
- `What dimensions are listed for the product?`
- `Is the object cylindrical, bottle-shaped, vase-shaped, or otherwise close to axisymmetric?`

Download pattern:

```bash
curl -L "IMAGE_URL" -o /Users/hivecrew/Desktop/<name>.png
```

## Primary script

Use the bundled script:

```bash
python3 scripts/build_revolved_obj.py   --image /Users/hivecrew/Desktop/inbox/bottle.png   --name bottle   --outdir /Users/hivecrew/Desktop/outbox   --height 225   --units mm
```

If no image is available and you still need a placeholder generic object, the script can synthesize a simple profile:

```bash
python3 scripts/build_revolved_obj.py   --generic bottle   --name bottle   --outdir /Users/hivecrew/Desktop/outbox   --height 225   --units mm
```

## What the script does

- Detect the object silhouette from alpha or from contrast against the border background.
- Extract left/right contour points and derive a centerline and radius profile.
- Save coordinate points to CSV.
- Generate a revolved mesh with UVs and caps.
- Build a texture strip from the reference image when possible.
- Create a dimensioned drawing with front, side, top, and isometric views.
- Save an analysis JSON summarizing scale, dimensions, mesh size, and file outputs.

## Important defaults and heuristics

- Always set a real dimension when you can find one, usually overall height.
- If the page lists dimensions, pass the known height with `--height` and the proper `--units`.
- If dimensions are unknown, the script still works, but the drawing dimensions are proportional estimates based on the provided height value.
- For transparent PNGs, alpha is used directly.
- For flat-background JPG/PNG images, the script estimates background color from the border.

## Validation checklist

After generating the files:

1. Open `*_drawing.png` with `read_file` and verify the silhouette and dimensions look plausible.
2. Inspect `*_analysis.json` for mesh counts and extracted bounds.
3. If the mask is wrong, rerun with a different `--bg-threshold`.
4. If the top or bottom is too sharp, lower smoothing with `--smooth-passes 1`.
5. If the object is visibly asymmetric, do not force this workflow; ask for more views or explain the limitation.

## Limits

This skill is intentionally narrow and reliable. It is for quick OBJ generation from one image of a mostly revolved object, not for arbitrary photogrammetry or sculpting.

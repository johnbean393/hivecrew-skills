# Generic object search prompts

Use this file only when no reference image is provided.

## Goal

Find a clean front or side product image for an object that can be approximated as a surface of revolution.

## High-signal queries

- `<object> front view isolated white background`
- `<object> product photo side view dimensions`
- `site:amazon.com <object> dimensions`
- `site:walmart.com <object> bottle jar cup vase`

## Page-check questions for `extract_info_from_webpage`

- Does the page contain a clear product image suitable for silhouette extraction?
- What overall height/diameter dimensions are listed?
- Is the object approximately axisymmetric?

## Download reminder

After identifying the image URL, download it with shell tools, for example:

```bash
curl -L "https://example.com/image.png" -o /Users/hivecrew/Desktop/reference.png
```

#!/usr/bin/env python3
"""
Create a structured prompt/specification for generating an infographic with the
environment's generate_image tool.

This script does NOT call external model APIs. It helps prepare a concise,
well-structured prompt plus a small JSON spec that an agent can feed into the
`generate_image` tool.
"""

import argparse
import json
from pathlib import Path

INFOGRAPHIC_TYPES = [
    "statistical", "timeline", "process", "comparison", "list",
    "geographic", "hierarchical", "anatomical", "resume", "social"
]

STYLE_PRESETS = [
    "corporate", "healthcare", "technology", "nature", "education",
    "marketing", "finance", "nonprofit"
]

PALETTE_PRESETS = ["wong", "ibm", "tol"]
ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]

STYLE_DESCRIPTIONS = {
    "corporate": "navy, steel blue, and gold accents; clean business look",
    "healthcare": "clean medical blue/cyan palette with trustworthy clinical styling",
    "technology": "modern blue/slate/violet palette with sleek tech visuals",
    "nature": "greens and earth tones with organic visual language",
    "education": "clear academic layout with blue and warm accent colors",
    "marketing": "bold vibrant coral, teal, and yellow for high visual energy",
    "finance": "restrained navy and gold with strong clarity and professionalism",
    "nonprofit": "warm human-centered palette with orange, sage, and sand tones",
}

PALETTE_DESCRIPTIONS = {
    "wong": "Wong colorblind-safe palette",
    "ibm": "IBM accessible palette",
    "tol": "Tol qualitative palette",
}


def build_prompt(args):
    lines = [f"Create a professional {args.type or 'general'} infographic."]
    lines.append(f"Topic: {args.prompt}")
    if args.doc_type:
        lines.append(f"Use case: {args.doc_type}")
    if args.style:
        lines.append(f"Style: {args.style} — {STYLE_DESCRIPTIONS.get(args.style, args.style)}")
    if args.palette:
        lines.append(f"Color palette: {args.palette} — {PALETTE_DESCRIPTIONS.get(args.palette, args.palette)}")
    lines.extend([
        "Layout: clear hierarchy, clean spacing, balanced composition, easy-to-scan infographic structure.",
        f"Background: {args.background}.",
        "Typography: bold readable headline, short labels, no tiny text, no overlapping text.",
        "Accessibility: strong contrast, colorblind-friendly distinctions, use labels/shapes not color alone.",
        "Output: polished publication-ready infographic illustration.",
    ])
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Prepare a prompt/spec for the environment generate_image tool")
    p.add_argument("prompt", help="Description of the infographic topic/content")
    p.add_argument("-o", "--output", required=True, help="Path to save the generated prompt/spec JSON")
    p.add_argument("--type", "-t", choices=INFOGRAPHIC_TYPES)
    p.add_argument("--style", "-s", choices=STYLE_PRESETS)
    p.add_argument("--palette", "-p", choices=PALETTE_PRESETS)
    p.add_argument("--background", "-b", default="white")
    p.add_argument("--doc-type", default="default")
    p.add_argument("--aspect-ratio", default="3:4", choices=ASPECT_RATIOS)
    args = p.parse_args()

    prompt = build_prompt(args)
    spec = {
        "tool": "generate_image",
        "aspectRatio": args.aspect_ratio,
        "prompt": prompt,
        "notes": [
            "Call the environment's generate_image tool with this prompt.",
            "If text density causes issues, shorten the copy and regenerate.",
            "Use web_search/read_webpage_content before generation if current facts are needed."
        ]
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() == '.json':
        out.write_text(json.dumps(spec, indent=2))
    else:
        out.write_text(prompt + "\n")

    print(f"Saved infographic generation spec to: {out}")
    print("Next step: call the environment's generate_image tool using the saved prompt/spec.")


if __name__ == '__main__':
    main()

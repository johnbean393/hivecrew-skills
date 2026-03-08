---
name: infographics
description: "Create professional infographics using the environment's built-in tools. Use web_search/read_webpage_content for research and generate_image for infographic creation. Supports multiple infographic types, style presets, and colorblind-safe palettes."
allowed-tools: [Read, Write, Edit, Bash]
---

# Infographics

## Overview

Create professional infographics by combining the environment's built-in tools:

- **Research tools**: `web_search`, `read_webpage_content`, `extract_info_from_webpage`
- **Image generation tool**: `generate_image`
- **File tools**: `read_file`, `move_file`, `run_shell`

This skill should **not rely on external model APIs, OpenRouter, or custom HTTP image-generation scripts**. Instead, research the topic if needed, then call the environment's **`generate_image`** tool directly with a carefully structured prompt.

## When to Use This Skill

Use this skill when you need:
- Statistical/data infographics
- Timelines
- Process/how-to graphics
- Comparisons
- List-based infographics
- Geographic/map-like infographic layouts
- Hierarchical/pyramid visuals
- Anatomical/visual-metaphor explainers
- Resume/professional infographic layouts
- Social-media infographic graphics

## Core Workflow

1. **Clarify the goal**
   - Identify the infographic type, audience, output format, and intended use.
2. **Research if accuracy matters**
   - Use `web_search` to find recent sources.
   - Use `read_webpage_content` or `extract_info_from_webpage` to extract the exact facts/statistics needed.
   - Prefer authoritative sources and cite years/sources in the prompt when helpful.
3. **Structure the content**
   - Reduce the content to a concise title, 3-7 key points, and any key numbers/dates.
   - Avoid excessive text; image models perform better with shorter, high-signal copy.
4. **Generate with `generate_image`**
   - Write a precise prompt specifying:
     - infographic type
     - layout
     - content hierarchy
     - style/colors
     - accessibility requirements
     - aspect ratio
     - exact text that must appear
5. **Review and refine**
   - If the output has text/layout issues, regenerate with a simpler prompt, shorter text, clearer hierarchy, or fewer elements.

## Important Rules

- Prefer **tool-native generation** with `generate_image` over shell scripts that call outside APIs.
- Prefer **tool-native research** with `web_search` and `read_webpage_content` over ad-hoc browsing.
- Keep copy short and scannable.
- Ask for a clean background, strong hierarchy, and readable typography.
- When exact wording matters, explicitly provide the text to include.
- If the model struggles with dense text, reduce the amount of text and emphasize iconography, labels, and large numbers.

## Recommended Prompt Template for `generate_image`

Use a prompt like this and adapt it to the user's request:

```text
Create a professional [TYPE] infographic.

Topic: [TOPIC]
Audience: [AUDIENCE]
Goal: [GOAL]

Layout:
- [overall layout]
- clear visual hierarchy
- clean spacing
- easy to scan

Required content:
- Title: [TITLE]
- Section 1: [TEXT]
- Section 2: [TEXT]
- Section 3: [TEXT]
- Key statistic/date/callout: [TEXT]

Design style:
- [STYLE PRESET]
- [COLOR PALETTE]
- white or very light background
- polished editorial infographic look
- accessible contrast
- colorblind-friendly distinctions

Typography:
- bold readable headline
- short labels only
- no tiny text
- no overlapping text

Output:
- high-quality infographic illustration
- balanced composition
- publication-ready
```

## Aspect Ratio Guidance

Choose an aspect ratio appropriate to the use case when calling `generate_image`:

- `1:1` — social posts, compact cards
- `4:5` — portrait social posts
- `3:4` — poster-like infographic
- `16:9` — presentation slide infographic
- `9:16` — story/mobile vertical infographic

## Infographic Type Guidance

### Statistical
Use for numbers, metrics, percentages, and trends.
Emphasize large numbers, simple charts, and clear labels.

### Timeline
Use chronological milestones with year/date markers and a clear visual path.

### Process
Use numbered steps, arrows, and short action phrases.

### Comparison
Use side-by-side columns with matching comparison rows.

### List
Use numbered items or icon-led cards.

### Geographic
Use map-inspired layouts only when geography is central; simplify labels.

### Hierarchical
Use stacked levels, pyramid layouts, or tree structures.

### Anatomical / Visual Metaphor
Use a central metaphor with callout labels.

### Resume / Professional
Use sections for profile, skills, experience, and highlights.

### Social
Use minimal copy, bold headline, and one or two core stats/messages.

## Style Presets

- `corporate` — navy, steel blue, gold accents
- `healthcare` — blue, cyan, clean clinical feel
- `technology` — blue, slate, violet accents
- `nature` — greens, earth tones
- `education` — blue with warm accent colors
- `marketing` — coral, teal, yellow, bold and vibrant
- `finance` — navy, gold, restrained business look
- `nonprofit` — warm orange, sage, sand, human-centered tone

## Colorblind-Safe Palettes

- `wong`
- `ibm`
- `tol`

When accessibility matters, explicitly ask for one of these palettes and tell the model to use labels/shapes, not color alone, to communicate differences.

## Research Workflow

Use research when the infographic needs current facts or statistics.

Suggested sequence:
1. `web_search` for the topic
2. `read_webpage_content` for the strongest sources
3. Distill 3-7 core facts
4. Put only the most important facts into the image-generation prompt

## Deliverables

Save final outputs in the requested destination. If you create prompt notes or a fact summary, save them alongside the image when useful.

## References

See the reference files in `references/` for:
- infographic type ideas
- design principles
- color palette suggestions

## Deprecated Components

The older OpenRouter/Nano Banana workflow is deprecated in this environment. Do not require:
- `OPENROUTER_API_KEY`
- custom `requests` calls to model APIs
- external image-generation HTTP endpoints

Use the environment tools directly instead.

# Color System Guide

Professional color palette and usage guidelines for research reports.

## Palette Overview

| Role | Hex Code | RGB | Usage |
|------|----------|-----|-------|
| Primary | #243A5E | rgb(36, 58, 94) | Section titles, major headings |
| Secondary | #4A6FA5 | rgb(74, 111, 165) | Subheadings, labels, secondary text |
| Accent | #C9A24D | rgb(201, 162, 77) | Key metrics, emphasis, separators |
| Body | #1C1C1C | rgb(28, 28, 28) | Paragraphs, descriptions, content |
| Background | #F6F8FA | rgb(246, 248, 250) | Table headers, light backgrounds |

---

## Color Application

### Section Titles (Primary #243A5E)
Apply to all major section headings:

```
## Executive Summary
## Business Overview
## Financial Analysis
```

### Subheadings (Secondary #4A6FA5)
Use for subsection headers and labels:

```
### Revenue Analysis
### Margin Drivers
### Segment Performance
```

### Key Metrics (Accent #C9A24D)
Reserve for:
- Key numbers in executive summary tables
- Highlighting critical assumptions
- Separator lines between sections
- Bullet points for key takeaways

**Do NOT use accent for:**
- Regular body text
- Large blocks of text
- Background fills (too dominant)

### Body Text (#1C1C1C)
Standard color for all content text:
- Paragraphs
- Table content
- Chart descriptions
- Analysis text

### Table Backgrounds (#F6F8FA)
Apply to:
- Table header rows
- Alternating row backgrounds (optional)
- Callout boxes
- Figure backgrounds

---

## Usage Rules

### The Accent Color Rule

**Use accent sparingly** - it's for emphasis, not decoration.

✅ **Correct uses:**
- Highlighting the final "BUY" rating
- Drawing attention to key assumptions
- One or two critical numbers per table
- Section dividers

❌ **Incorrect uses:**
- Coloring entire columns
- Multiple highlighted metrics per section
- Decorative borders or lines
- Background fills for text

### No Performance Signaling

**Never use red/green for performance signaling.**

This ensures:
- Accessibility for colorblind readers
- Professional, neutral presentation
- Print-friendly output

**Instead of colors, use:**
- Directional indicators: ↑ ↓ →
- Text labels: "Outperform" / "Underperform"
- Formatting: Bold for emphasis
- Context: Explain performance in text

### Contrast Requirements

Maintain readability with proper contrast:
- Body text (#1C1C1C) on white: Excellent contrast
- Primary (#243A5E) on white: Excellent contrast
- Secondary (#4A6FA5) on white: Good contrast
- Accent (#C9A24D) on white: For emphasis only, not body text

---

## Table Styling

### Header Row
```
┌─────────────────────────────────────────────────────────────┐
│ #F6F8FA background                                           │
│ Metric    │ 2022  │ 2023  │ 2024E │ CAGR   │ ← Primary text │
└─────────────────────────────────────────────────────────────┘
```

### Data Rows
```
│ Revenue   │ $1.0B │ $1.2B │ $1.4B │ 18.3%  │ ← Body text    │
│ Margin    │ 35.2% │ 36.1% │ 37.0% │ --     │                │
│           │       │       │       │        │                │
│ *Key metric: 18% CAGR*                       ← Accent text  │
```

### Border and Separator Lines
- Use subtle borders (1px, #4A6FA5 or #CCCCCC)
- Accent color for major section separators
- Avoid heavy or decorative borders

---

## Chart Color Application

### Bar Charts
For categorical comparisons:
1. Use Primary (#243A5E) for primary/subject data
2. Use Secondary (#4A6FA5) for comparison data
3. Use Accent (#C9A24D) for target/highlight only

### Line Charts
- Primary lines: #243A5E
- Secondary/comparison lines: #4A6FA5
- Target/reference lines: #C9A24D (dashed)

### Pie/Donut Charts
- Primary: #243A5E
- Secondary: #4A6FA5
- Accent: #C9A24D
- Additional segments: Use grayscale or tints

---

## Print Considerations

### Grayscale Readability
All colors should remain distinguishable in grayscale:
- Primary: Dark gray (good contrast)
- Secondary: Medium gray
- Accent: Light-medium gray
- Body: Near black

### Paper Quality
Design assumes standard office printing:
- Colors may appear slightly different on paper
- High contrast ensures readability on all media
- Avoid subtle color distinctions

---

## Quick Reference

| Element | Color | Notes |
|---------|-------|-------|
| Section titles | #243A5E | Primary, bold |
| Subheadings | #4A6FA5 | Secondary, regular weight |
| Body text | #1C1C1C | Dark, readable |
| Key emphasis | #C9A24D | Sparingly, accent |
| Table headers | #F6F8FA | Background fill |
| Borders | #CCCCCC or #4A6FA5 | Subtle |
| Positive indicators | Text: "Outperform" | No green |
| Negative indicators | Text: "Underperform" | No red |

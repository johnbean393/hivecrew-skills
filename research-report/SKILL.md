---
name: research-report
description: Create professional research reports with visual storytelling, Mermaid diagrams, generated infographics, structured analysis, and manual-LaTeX PDF-ready formatting. Use when generating investment research, market analysis, industry reports, or any formal research deliverable requiring tables, diagrams, frameworks, and professional presentation. Triggers include requests for equity research, sector analysis, competitive analysis, or any report intended for institutional or professional audiences.
---

# Research Report

Create professional research reports with integrated visual elements, structured analysis, and production-quality PDF output.

## Core Principles

1. **Visual storytelling**: Every major section should advance the argument with analytical visuals such as tables, Mermaid diagrams, comparison matrices, or infographics.
2. **Evidence before opinion**: Clearly distinguish facts, assumptions, analysis, and conclusions.
3. **PDF-first authoring**: Optimize for a polished PDF from the start rather than treating PDF as an afterthought.
4. **Visual-to-text balance**: Unless the user requests otherwise, target a roughly **4:6 diagram/image-to-text ratio** across the report. In practice, aim for about **40% visual content and 60% text** by page real estate or content blocks.
5. **Conservative, print-safe design**: Use restrained colors, clean spacing, and professional typography suitable for institutional readers.

## Report Structure

### Required Sections

1. **Executive Summary** - Key thesis, metrics, and conclusions
2. **Subject Overview** - Core subject/entity description and context
3. **Industry & Competition** - Market landscape and positioning
4. **Analysis** - Deep-dive into key metrics and drivers
5. **Risks** - Structured risk assessment
6. **Conclusion** - Summary and actionable insights

### Section Flexibility

Adapt sections to the research context:
- **Company analysis**: Include Financial Analysis section
- **Sector research**: Include Market Dynamics section
- **Competitive intelligence**: Expand Industry & Competition
- **Policy research**: Include Regulatory Landscape section

## Default Visual Mix

Unless the user explicitly requests otherwise:

- Aim for a **roughly 4:6 diagram/image-to-text ratio** across the report.
- Ensure the report uses both **Mermaid diagrams** and **generated infographics/illustrations** whenever they materially improve clarity.
- Treat visuals as analytical assets, not decoration.
- Caption every figure and table explicitly, and reference each one in the surrounding prose.

### Visual Expectations by Type

- **Mermaid diagrams**: Use for workflows, operating models, market maps, process flows, decision trees, structures, dependency chains, and framework overviews.
- **Generated infographics**: Use for conceptual overviews, landscape summaries, timeline scenes, stylized ecosystem maps, and section-leading editorial visuals.
- **Tables and matrices**: Use for metrics, comparisons, scoring frameworks, and risk assessments.

## Visual Elements

Each major section must include at least one visual element, and the overall report should maintain the default visual mix above unless the user directs otherwise.

| Section | Recommended Visuals |
|---------|---------------------|
| Executive Summary | Compact metrics table, thesis summary box, simple infographic |
| Subject Overview | Mermaid structure diagram, capability map, generated overview visual |
| Industry & Competition | Positioning matrix, competitor table, ecosystem diagram |
| Analysis | Historical performance tables, bridge diagrams, driver trees |
| Risks | Risk matrix, scenario table, dependency/trigger diagram |
| Conclusion | Summary scorecard, recommendation table, closing synthesis graphic |

**Captions**: Use explicit captions like `Table: Key financial metrics overview` or `Figure: Revenue structure by segment`.

**Reference**: See [references/visual-elements.md](references/visual-elements.md) for detailed guidance on visual types, Mermaid usage, infographic generation, and PDF embedding.

## Preferred PDF Production Method

Use a **manual LaTeX workflow compiled with XeLaTeX** as the default method for final research-report PDFs.

### Why this is the default

- It gives the best control over page layout, headings, spacing, tables, captions, and figure placement.
- It preserves vector diagrams cleanly in the PDF.
- It is more reliable on this machine than markdown-first PDF pipelines for complex report layouts.

### Default PDF Workflow

1. **Plan the report structure** and decide where visuals belong before drafting.
2. **Draft the analysis** and prepare the numerical tables.
3. **Write Mermaid diagrams** for flows, structures, and frameworks.
4. **Render Mermaid diagrams to SVG**, then convert SVG to PDF for LaTeX embedding when needed so diagrams remain crisp and vector-based.
5. **Generate infographics or editorial visuals** when they improve comprehension.
6. **Compose the final report in LaTeX** with explicit figure/table placement and captioning.
7. **Compile with XeLaTeX** and run the compilation twice for stable references and layout.

### LaTeX Authoring Standard

Prefer a direct LaTeX composition approach over automatic markdown-to-PDF conversion for the final deliverable.

Recommended package set, subject to local availability:
- `geometry`
- `fontspec`
- `xcolor`
- `graphicx`
- `booktabs`
- `longtable`
- `tabularx`
- `array`
- `float`
- `caption`
- `hyperref`
- `fancyvrb` or `listings`
- `multirow` when needed

### Reliability Rules for PDF Rendering

- Prefer **XeLaTeX** as the primary compiler.
- Prefer installed sans-serif fonts such as **Helvetica** or **Arial** when portability matters.
- If optional packages such as `titlesec` or `svg` are unavailable, **simplify the styling rather than changing the whole PDF pipeline**.
- If direct SVG inclusion is fragile, convert Mermaid SVGs to PDF and embed them with `\includegraphics`.
- Compile twice before final review.
- Validate the final PDF before returning it: use `verapdf` when available for PDF/A or PDF/UA conformance and accessibility checks, or `pdfcpu validate -mode strict` as a structural validation fallback.
- If accessibility is a requirement, prefer `verapdf` with the relevant PDF/UA profile and treat validation failures as blockers.
- Treat Pandoc-based PDF generation as a **fallback**, not the primary method, for complex reports.

## Color System

Use this palette for all visual elements:

| Role | Hex Code | Usage |
|------|----------|-------|
| Primary (titles) | #243A5E | Section headings |
| Secondary (subsections) | #4A6FA5 | Subheadings, labels |
| Accent (emphasis) | #C9A24D | Key metrics, separators |
| Body text | #1C1C1C | Paragraphs, descriptions |
| Table background | #F6F8FA | Table headers, backgrounds |

**Rules**:
- Accent color only for emphasis and structure
- Never use red/green for performance signaling
- Maintain conservative contrast suitable for print

**Reference**: See [references/color-system.md](references/color-system.md) for detailed usage guidelines.

## Writing Standards

### Analytical Rigor

- Clearly separate facts, assumptions, analysis, and conclusions.
- Every conclusion must be traceable to presented analysis.
- Discuss both upside drivers and downside risks.
- Avoid speculative or promotional language.

### Formatting for PDF

- Do NOT break lines mid-sentence.
- Paragraph breaks only at logical section boundaries.
- Bullet points should be used sparingly and left-aligned.
- Tables must be clean, readable, and information-dense.
- Prefer vector diagrams over rasterized line art.
- Every figure and table must have a caption.
- Reference visuals explicitly in the text.
- Avoid unnecessary Unicode symbols if font support may be unreliable.
- Keep page breaks deliberate and avoid orphaned headings.

## Workflow

1. **Gather context** - Collect data, metrics, and source materials.
2. **Outline structure** - Define sections, key claims, and the visual plan.
3. **Allocate visuals** - Distribute Mermaid diagrams, infographics, and tables to maintain the default 4:6 visual-to-text balance unless the user asks for something else.
4. **Draft sections** - Write the analysis and connect every major claim to supporting evidence.
5. **Create visuals** - Build Mermaid diagrams, tables, and generated infographics as needed.
6. **Compose in LaTeX** - Assemble the final report with controlled layout and captions.
7. **Compile and review** - Run XeLaTeX twice, validate the PDF with `verapdf` or `pdfcpu`, review the output, and fix layout, accessibility, or structural issues.

## Output Quality Bar

The final report should:
- Resemble a professional institutional research deliverable.
- Enable readers to evaluate the thesis through text and visuals alone.
- Use Mermaid diagrams and generated infographics when they improve clarity.
- Maintain the default 4:6 diagram/image-to-text balance unless the user instructs otherwise.
- Be suitable for direct PDF rendering without post-editing.
- Pass a final PDF validation check and not be returned if it is malformed or fails required accessibility validation.

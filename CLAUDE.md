# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Notebook PDF pattern generator for Spanish handmade bookbinding. Generates customizable notebook pages with various patterns (lined, dotted, squared, Cornell, isometric, hexagonal) following Spanish industry standards.

Self-contained web application in `index.html` - no dependencies required, runs entirely in the browser.

## Running the Application

```bash
# Open in browser - no dependencies or installation required
open index.html
```

Or simply double-click `index.html` to open in your default browser.

## Architecture

### Web App (`index.html`)
Single-file, self-contained web application with no backend dependencies.

**Structure:**
- Uses jsPDF library (CDN) for client-side PDF generation
- Live canvas-based preview that updates on input change
- All settings stored in JavaScript config object via `getConfig()`
- Pattern drawing split between PDF generation (`drawPattern()`) and preview rendering (`drawPreviewPattern()`)

**Key functions:**
- `generatePDF()` - Main PDF generation with imposition support (1, 2, 4 pages per sheet)
- `updatePreview()` - Redraws canvas preview on any config change
- `drawPreviewPattern()` - Canvas rendering for all pattern types
- Pattern-specific drawers: `drawLined()`, `drawDotted()`, `drawSquared()`, `drawCornell()`, `drawIsometric()`, `drawHexagonal()`

**Important constants:**
- `PAGE_SIZES` - Page dimensions in mm (A4, A5, A6, B5, Letter)
- `PREVIEW_MAX_HEIGHT` - Canvas preview height limit (280px)
- `PREVIEW_SCALE` - Pixels per mm for preview (1.5)

## PDF Generation

**Imposition/Pages per sheet:**
- 1 page/sheet - Single page, no folding
- 2 pages/sheet - Side-by-side for folding
- 4 pages/sheet - Saddle-stitch booklet layout

**Pattern types:**
- `lined` - Horizontal lines with optional header line
- `dotted` - Dot grid with configurable spacing
- `squared` - Grid of squares (cuadrícula)
- `cornell` - Cornell note-taking method (cue column + summary area)
- `isometric` - 30° isometric grid for technical drawing
- `hexagonal` - Honeycomb pattern
- `blank` - No pattern

## Spanish Industry Standards

Default values follow Spanish handmade notebook conventions:
- Page size: A5 (148×210mm) - most popular for artisanal notebooks
- Pattern: Cuadrícula (5mm squares) - Spanish standard
- Pauta: 8mm line spacing for lined notebooks
- Line color: 75% gray - discrete but visible
- Line weight: 0.3pt - standard quality
- Margins: 10mm top/bottom, 15mm left (binding), 10mm right

## Modifying Patterns

When adding new patterns or options:

1. Update both PDF generation AND preview rendering
   - Add pattern drawer function (e.g., `drawMyPattern()`)
   - Add preview renderer (in `drawPreviewPattern()` switch)
   - Update HTML `<select>` with new option

2. Keep margin calculations consistent: subtract margins from drawable area

3. Use proper units:
   - jsPDF uses mm directly
   - Canvas preview: scale with `spacing * PREVIEW_SCALE`

## Fold Lines

Optional dashed lines showing where to cut/fold for multi-page sheets:
- Only visible when `pages_per_sheet > 1`
- Rendered as light gray (#e6e6e6) dashed lines
- Toggle controlled by `fold_lines` option

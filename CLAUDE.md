# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Notebook PDF pattern generator for Spanish handmade bookbinding. Generates customizable notebook pages with various patterns (lined, dotted, squared, Cornell, isometric, hexagonal) following Spanish industry standards.

**Three implementations:**
- `generate_patterns.py` - Original simple CLI script
- `generate.py` - Terminal UI (TUI) using Textual library
- `index.html` - Self-contained web app (recommended)

## Running the Applications

**Web app (recommended):**
```bash
# Open in browser - no dependencies required
open index.html
```

**Python TUI:**
```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt

# Run TUI
python3 generate.py
```

**Original CLI:**
```bash
python3 generate_patterns.py
```

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

### Python TUI (`generate.py`)
Terminal UI using Textual framework with `OptionList` widgets.

**Known issues:**
- Rendering problems in iTerm2 with some Textual widgets
- `ListView` with custom `ListItem` subclasses didn't render properly
- Switched to `OptionList` with `Option` objects for better compatibility

**Configuration:**
- `CONFIG_SCHEMA` - Complete schema with all options, labels, descriptions
- Spanish defaults: A5 page, 5mm cuadrícula, 8mm pauta, 75% gray

### PDF Generation
Both Python and JavaScript use similar algorithms for pattern generation:

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

1. **Web app:** Update both PDF generation AND preview rendering
   - Add pattern drawer function (e.g., `drawMyPattern()`)
   - Add preview renderer (in `drawPreviewPattern()` switch)
   - Update HTML `<select>` with new option

2. **Python TUI:** Update `CONFIG_SCHEMA` and add pattern function

3. Keep margin calculations consistent: subtract margins from drawable area

4. Use proper units:
   - Python: ReportLab uses points, convert with `* mm`
   - JavaScript: jsPDF uses mm directly
   - Canvas preview: scale with `spacing * scale`

## Fold Lines

Optional dashed lines showing where to cut/fold for multi-page sheets:
- Only visible when `pages_per_sheet > 1`
- Rendered as light gray (#e6e6e6) dashed lines
- Toggle controlled by `fold_lines` option

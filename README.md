# Notebook Pattern Generator

A web-based PDF pattern generator for Spanish handmade bookbinding. Create customizable notebook pages with various patterns following Spanish industry standards.

## Features

- **Multiple Pattern Types:**
  - Lined (pauta) - Horizontal lines with optional header
  - Dotted - Configurable dot grid
  - Squared (cuadrícula) - Grid of squares
  - Cornell - Cornell note-taking method layout
  - Isometric - 30° grid for technical drawing
  - Hexagonal - Honeycomb pattern
  - Blank - No pattern

- **Flexible Configuration:**
  - Multiple page sizes (A4, A5, A6, B5, Letter)
  - Customizable margins
  - Adjustable line spacing, dot spacing, and grid size
  - Color and line weight controls
  - Portrait/landscape orientation

- **Imposition Support:**
  - 1 page per sheet - Single page printing
  - 2 pages per sheet - Side-by-side for folding
  - 4 pages per sheet - Saddle-stitch booklet layout
  - Optional fold lines for cutting/folding guides

- **Live Preview:**
  - Real-time canvas preview
  - Instant updates as you change settings

- **Favorites System:**
  - Save your favorite configurations
  - Quick access to commonly used settings
  - Stored locally in your browser

## Usage

1. **Open the application:**
   - Simply open `index.html` in your web browser
   - No installation or dependencies required
   - Works completely offline

2. **Configure your pattern:**
   - Select pattern type from the dropdown
   - Adjust page size, margins, and spacing
   - Customize colors and line weights
   - Toggle features like header lines and fold lines

3. **Preview and generate:**
   - See live preview on the right side
   - Click "Generate PDF" to download your notebook pages
   - Save configurations as favorites for quick access

## Spanish Industry Standards

Default values follow Spanish handmade notebook conventions:

- **Page size:** A5 (148×210mm) - most popular for artisanal notebooks
- **Pattern:** Cuadrícula (5mm squares) - Spanish standard
- **Pauta:** 8mm line spacing for lined notebooks
- **Line color:** 75% gray - discrete but visible
- **Line weight:** 0.3pt - standard quality
- **Margins:** 10mm top/bottom, 15mm left (binding), 10mm right

## Technical Details

- **Single-file application:** Everything is contained in `index.html`
- **No backend required:** Runs entirely in the browser
- **Client-side PDF generation:** Uses jsPDF library (loaded from CDN)
- **Local storage:** Favorites are saved in browser localStorage
- **No data collection:** All processing happens locally

## Browser Compatibility

Works in all modern browsers that support:
- HTML5 Canvas
- ES6 JavaScript
- localStorage API

## License

Feel free to use and modify for your bookbinding projects!

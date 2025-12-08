#!/usr/bin/env python3
"""
Enhanced Notebook PDF Generator
Generates customizable notebook pages for handmade bookbinding.
Defaults follow Spanish handmade notebook industry standards.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A5, A6, B5, LETTER, landscape, portrait
from reportlab.lib.units import mm
from reportlab.lib.colors import Color
import math

# =============================================================================
# CONSTANTS & DEFAULTS (Spanish Handmade Notebook Industry Standards)
# =============================================================================

PAGE_SIZES = {
    "a4": A4,
    "a5": A5,
    "a6": A6,
    "b5": B5,
    "letter": LETTER,
}

PATTERNS = {
    "lined": "Líneas horizontales",
    "dotted": "Puntos (bullet journal)",
    "squared": "Cuadrícula",
    "blank": "En blanco",
    "cornell": "Método Cornell (notas)",
    "isometric": "Isométrico (dibujo técnico)",
    "hexagonal": "Hexagonal",
}

# Spanish industry defaults
DEFAULTS = {
    "page_size": "a5",           # Most popular for cuadernos artesanales
    "orientation": "portrait",
    "pattern": "squared",        # Cuadrícula is very common in Spain
    "line_spacing": 8,           # 8mm standard for pauta española
    "dot_spacing": 5,            # 5mm for bullet journal
    "square_size": 5,            # 5mm cuadrícula estándar
    "margin_top": 10,
    "margin_bottom": 10,
    "margin_left": 10,
    "margin_right": 10,
    "binding_margin": 5,         # Extra margin for binding side
    "line_color_rgb": (0.75, 0.75, 0.75),  # Light gray (gris suave)
    "line_weight": 0.3,          # Thin lines
    "pages": 32,                 # Common signature count
    "pages_per_sheet": 1,        # 1, 2, or 4 for imposition
    "header_line": False,        # Línea de encabezado
    "page_numbers": False,
    "bleed": 0,                  # Bleed for professional printing
    "punch_holes": "none",       # none, 2-hole, 4-hole
}


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_pagesize(choice, orientation):
    """Get page dimensions based on size choice and orientation."""
    size = PAGE_SIZES.get(choice.lower(), A5)
    if orientation == "landscape":
        return landscape(size)
    return portrait(size)


def parse_color(rgb_tuple):
    """Convert RGB tuple (0-1 range) to ReportLab Color."""
    return Color(*rgb_tuple)


def input_with_default(prompt, default, cast_type=str):
    """Get user input with a default value and type casting."""
    value = input(f"{prompt} [{default}]: ").strip()
    if not value:
        return default if cast_type == str else cast_type(default)
    try:
        return cast_type(value)
    except ValueError:
        print(f"  ⚠ Valor inválido, usando default: {default}")
        return default if cast_type == str else cast_type(default)


def input_yes_no(prompt, default=False):
    """Get yes/no input from user."""
    default_str = "s" if default else "n"
    value = input(f"{prompt} (s/n) [{default_str}]: ").strip().lower()
    if not value:
        return default
    return value in ["s", "si", "sí", "y", "yes", "true", "1"]


# =============================================================================
# DRAWING FUNCTIONS
# =============================================================================

def draw_lined(c, x_start, y_start, width, height, config):
    """Draw horizontal lines (pauta)."""
    spacing = config["line_spacing"] * mm
    margin_top = config["margin_top"] * mm
    margin_bottom = config["margin_bottom"] * mm
    margin_left = config["margin_left"] * mm
    margin_right = config["margin_right"] * mm

    # Header line if enabled
    if config["header_line"]:
        header_y = y_start + height - margin_top
        c.setStrokeColor(parse_color(config["line_color_rgb"]))
        c.setLineWidth(config["line_weight"] * 1.5)
        c.line(x_start + margin_left, header_y,
               x_start + width - margin_right, header_y)
        c.setLineWidth(config["line_weight"])
        start_y = header_y - spacing * 2
    else:
        start_y = y_start + height - margin_top - spacing

    y = start_y
    while y > y_start + margin_bottom:
        c.line(x_start + margin_left, y, x_start + width - margin_right, y)
        y -= spacing


def draw_dotted(c, x_start, y_start, width, height, config):
    """Draw dot grid (punteado)."""
    spacing = config["dot_spacing"] * mm
    margin_top = config["margin_top"] * mm
    margin_bottom = config["margin_bottom"] * mm
    margin_left = config["margin_left"] * mm
    margin_right = config["margin_right"] * mm
    dot_radius = config["line_weight"] * 0.6

    c.setFillColor(parse_color(config["line_color_rgb"]))

    y = y_start + height - margin_top
    while y > y_start + margin_bottom:
        x = x_start + margin_left
        while x < x_start + width - margin_right:
            c.circle(x, y, dot_radius, fill=1, stroke=0)
            x += spacing
        y -= spacing


def draw_squared(c, x_start, y_start, width, height, config):
    """Draw grid/graph paper (cuadrícula)."""
    spacing = config["square_size"] * mm
    margin_top = config["margin_top"] * mm
    margin_bottom = config["margin_bottom"] * mm
    margin_left = config["margin_left"] * mm
    margin_right = config["margin_right"] * mm

    left = x_start + margin_left
    right = x_start + width - margin_right
    top = y_start + height - margin_top
    bottom = y_start + margin_bottom

    # Vertical lines
    x = left
    while x <= right:
        c.line(x, bottom, x, top)
        x += spacing

    # Horizontal lines
    y = bottom
    while y <= top:
        c.line(left, y, right, y)
        y += spacing


def draw_cornell(c, x_start, y_start, width, height, config):
    """Draw Cornell note-taking layout."""
    margin = config["margin_left"] * mm
    line_spacing = config["line_spacing"] * mm

    # Cornell proportions
    cue_column_width = width * 0.25  # Left column for cues (25%)
    summary_height = height * 0.15   # Bottom summary area (15%)

    c.setStrokeColor(parse_color(config["line_color_rgb"]))
    c.setLineWidth(config["line_weight"] * 2)

    # Vertical divider (cue column)
    cue_x = x_start + cue_column_width
    c.line(cue_x, y_start + summary_height, cue_x, y_start + height - margin)

    # Horizontal divider (summary area)
    c.line(x_start + margin, y_start + summary_height,
           x_start + width - margin, y_start + summary_height)

    # Light lines in note-taking area
    c.setLineWidth(config["line_weight"])
    y = y_start + height - margin - line_spacing
    while y > y_start + summary_height + margin:
        c.line(cue_x + margin/2, y, x_start + width - margin, y)
        y -= line_spacing


def draw_isometric(c, x_start, y_start, width, height, config):
    """Draw isometric grid for technical drawing."""
    spacing = config["square_size"] * mm
    margin = config["margin_left"] * mm

    left = x_start + margin
    right = x_start + width - margin
    top = y_start + height - margin
    bottom = y_start + margin

    # Calculate angles for isometric (30 degrees)
    angle = math.radians(30)
    dx = spacing
    dy = spacing * math.tan(angle)

    c.setStrokeColor(parse_color(config["line_color_rgb"]))
    c.setLineWidth(config["line_weight"])

    # Horizontal lines
    y = bottom
    while y <= top:
        c.line(left, y, right, y)
        y += dy * 2

    # Diagonal lines (left-leaning)
    x = left
    while x <= right + (top - bottom) / math.tan(angle):
        x1, y1 = x, bottom
        x2 = x - (top - bottom) / math.tan(angle)
        y2 = top
        # Clip to bounds
        if x2 < left:
            y2 = bottom + (x - left) * math.tan(angle)
            x2 = left
        if x1 > right:
            y1 = bottom + (x - right) * math.tan(angle)
            x1 = right
        if y1 >= bottom and y2 <= top:
            c.line(x1, y1, x2, y2)
        x += dx

    # Diagonal lines (right-leaning)
    x = left - (top - bottom) / math.tan(angle)
    while x <= right:
        x1, y1 = x, bottom
        x2 = x + (top - bottom) / math.tan(angle)
        y2 = top
        # Clip to bounds
        if x1 < left:
            y1 = bottom + (left - x) * math.tan(angle)
            x1 = left
        if x2 > right:
            y2 = bottom + (right - x) * math.tan(angle)
            x2 = right
        if y1 >= bottom and y2 <= top:
            c.line(x1, y1, x2, y2)
        x += dx


def draw_hexagonal(c, x_start, y_start, width, height, config):
    """Draw hexagonal grid."""
    size = config["square_size"] * mm  # Hexagon size
    margin = config["margin_left"] * mm

    c.setStrokeColor(parse_color(config["line_color_rgb"]))
    c.setLineWidth(config["line_weight"])

    # Hexagon dimensions
    hex_width = size * 2
    hex_height = size * math.sqrt(3)

    row = 0
    y = y_start + height - margin - size
    while y > y_start + margin + size:
        offset = (hex_width * 0.75) if row % 2 else 0
        x = x_start + margin + size + offset
        while x < x_start + width - margin - size:
            draw_hexagon(c, x, y, size)
            x += hex_width * 1.5
        y -= hex_height / 2
        row += 1


def draw_hexagon(c, cx, cy, size):
    """Draw a single hexagon centered at (cx, cy)."""
    points = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        x = cx + size * math.cos(angle)
        y = cy + size * math.sin(angle)
        points.append((x, y))

    path = c.beginPath()
    path.moveTo(points[0][0], points[0][1])
    for x, y in points[1:]:
        path.lineTo(x, y)
    path.close()
    c.drawPath(path, fill=0, stroke=1)


def draw_blank(c, x_start, y_start, width, height, config):
    """Draw nothing (blank page)."""
    pass


def draw_pattern(c, x_start, y_start, width, height, config):
    """Route to appropriate pattern drawing function."""
    pattern = config["pattern"]

    c.setStrokeColor(parse_color(config["line_color_rgb"]))
    c.setLineWidth(config["line_weight"])

    pattern_funcs = {
        "lined": draw_lined,
        "dotted": draw_dotted,
        "squared": draw_squared,
        "cornell": draw_cornell,
        "isometric": draw_isometric,
        "hexagonal": draw_hexagonal,
        "blank": draw_blank,
    }

    func = pattern_funcs.get(pattern, draw_squared)
    func(c, x_start, y_start, width, height, config)


def draw_punch_holes(c, page_width, page_height, hole_type, margin):
    """Draw punch hole guides."""
    if hole_type == "none":
        return

    c.setStrokeColor(Color(0.8, 0.8, 0.8))
    c.setLineWidth(0.5)

    hole_radius = 3 * mm
    x = margin / 2

    if hole_type == "2-hole":
        # Standard 2-hole (80mm apart, centered)
        center_y = page_height / 2
        positions = [center_y - 40*mm, center_y + 40*mm]
    elif hole_type == "4-hole":
        # Standard 4-hole (European)
        positions = [
            page_height * 0.15,
            page_height * 0.38,
            page_height * 0.62,
            page_height * 0.85,
        ]
    else:
        return

    for y in positions:
        c.circle(x, y, hole_radius, fill=0, stroke=1)


def draw_page_number(c, page_width, page_height, page_num, config):
    """Draw page number."""
    c.setFillColor(Color(0.5, 0.5, 0.5))
    c.setFont("Helvetica", 8)
    margin = config["margin_bottom"] * mm

    # Alternate position based on page number (for book binding)
    if page_num % 2 == 0:
        x = config["margin_left"] * mm
    else:
        x = page_width - config["margin_right"] * mm

    c.drawString(x, margin / 2, str(page_num))


# =============================================================================
# IMPOSITION / PAGES PER SHEET
# =============================================================================

def create_imposed_page(c, sheet_width, sheet_height, pages_per_sheet,
                        page_configs, start_page, config):
    """
    Create an imposed sheet with multiple pages.
    pages_per_sheet: 1, 2, or 4
    """
    if pages_per_sheet == 1:
        # Single page per sheet
        draw_pattern(c, 0, 0, sheet_width, sheet_height, config)
        if config["page_numbers"] and start_page > 0:
            draw_page_number(c, sheet_width, sheet_height, start_page, config)
        if config["punch_holes"] != "none":
            draw_punch_holes(c, sheet_width, sheet_height,
                           config["punch_holes"], config["margin_left"] * mm)

    elif pages_per_sheet == 2:
        # Two pages side by side (for folding in half)
        half_width = sheet_width / 2

        # Left page
        draw_pattern(c, 0, 0, half_width, sheet_height, config)
        if config["page_numbers"] and start_page > 0:
            draw_page_number(c, half_width, sheet_height, start_page, config)

        # Right page
        draw_pattern(c, half_width, 0, half_width, sheet_height, config)
        if config["page_numbers"] and start_page > 0:
            draw_page_number(c, half_width, sheet_height, start_page + 1, config)

        # Fold line
        c.setStrokeColor(Color(0.9, 0.9, 0.9))
        c.setLineWidth(0.2)
        c.setDash(3, 3)
        c.line(half_width, 0, half_width, sheet_height)
        c.setDash()

    elif pages_per_sheet == 4:
        # Four pages (booklet imposition for saddle stitch)
        half_width = sheet_width / 2
        half_height = sheet_height / 2

        # Top-left
        draw_pattern(c, 0, half_height, half_width, half_height, config)
        # Top-right
        draw_pattern(c, half_width, half_height, half_width, half_height, config)
        # Bottom-left
        draw_pattern(c, 0, 0, half_width, half_height, config)
        # Bottom-right
        draw_pattern(c, half_width, 0, half_width, half_height, config)

        # Fold lines
        c.setStrokeColor(Color(0.9, 0.9, 0.9))
        c.setLineWidth(0.2)
        c.setDash(3, 3)
        c.line(half_width, 0, half_width, sheet_height)
        c.line(0, half_height, sheet_width, half_height)
        c.setDash()


# =============================================================================
# MAIN PDF CREATOR
# =============================================================================

def create_notebook_pdf(filename, config):
    """Create the notebook PDF with all configured options."""
    page_width, page_height = get_pagesize(config["page_size"],
                                            config["orientation"])

    # Add bleed if specified
    bleed = config["bleed"] * mm
    total_width = page_width + 2 * bleed
    total_height = page_height + 2 * bleed

    c = canvas.Canvas(filename, pagesize=(total_width, total_height))

    total_pages = config["pages"]
    pages_per_sheet = config["pages_per_sheet"]
    sheets_needed = math.ceil(total_pages / pages_per_sheet)

    for sheet in range(sheets_needed):
        start_page = sheet * pages_per_sheet + 1

        # Offset drawing by bleed amount
        c.translate(bleed, bleed)

        create_imposed_page(c, page_width, page_height, pages_per_sheet,
                          None, start_page, config)

        c.translate(-bleed, -bleed)
        c.showPage()

    c.save()
    print(f"\n✅ PDF creado: {filename}")
    print(f"   📄 {sheets_needed} hojas ({total_pages} páginas)")
    print(f"   📐 Tamaño: {config['page_size'].upper()} {config['orientation']}")
    print(f"   🔲 Patrón: {PATTERNS[config['pattern']]}")


# =============================================================================
# INTERACTIVE CONFIGURATION
# =============================================================================

def get_user_config():
    """Interactive configuration wizard."""
    print("\n" + "=" * 60)
    print("📓 GENERADOR DE CUADERNOS ARTESANALES")
    print("   Configuración para encuadernación artesanal española")
    print("=" * 60)

    config = DEFAULTS.copy()

    # --- Page Setup ---
    print("\n📐 CONFIGURACIÓN DE PÁGINA")
    print("-" * 40)

    print("   Tamaños disponibles: A4, A5, A6, B5, Letter")
    config["page_size"] = input_with_default(
        "   Tamaño de página", DEFAULTS["page_size"]).lower()

    print("   Orientaciones: portrait (vertical), landscape (horizontal)")
    config["orientation"] = input_with_default(
        "   Orientación", DEFAULTS["orientation"]).lower()

    # --- Pattern ---
    print("\n🔲 PATRÓN")
    print("-" * 40)
    for key, desc in PATTERNS.items():
        marker = "→" if key == DEFAULTS["pattern"] else " "
        print(f"   {marker} {key}: {desc}")
    config["pattern"] = input_with_default(
        "   Elegir patrón", DEFAULTS["pattern"]).lower()

    # --- Pattern-specific spacing ---
    print("\n📏 ESPACIADO")
    print("-" * 40)
    if config["pattern"] == "lined":
        config["line_spacing"] = input_with_default(
            "   Interlineado en mm (pauta española estándar: 8)",
            DEFAULTS["line_spacing"], float)
        config["header_line"] = input_yes_no(
            "   ¿Incluir línea de encabezado?", DEFAULTS["header_line"])
    elif config["pattern"] == "dotted":
        config["dot_spacing"] = input_with_default(
            "   Separación de puntos en mm", DEFAULTS["dot_spacing"], float)
    elif config["pattern"] in ["squared", "isometric", "hexagonal"]:
        config["square_size"] = input_with_default(
            "   Tamaño de celda en mm (cuadrícula estándar: 5)",
            DEFAULTS["square_size"], float)
    elif config["pattern"] == "cornell":
        config["line_spacing"] = input_with_default(
            "   Interlineado del área de notas en mm",
            DEFAULTS["line_spacing"], float)

    # --- Margins ---
    print("\n📍 MÁRGENES (en mm)")
    print("-" * 40)
    config["margin_top"] = input_with_default(
        "   Margen superior", DEFAULTS["margin_top"], float)
    config["margin_bottom"] = input_with_default(
        "   Margen inferior", DEFAULTS["margin_bottom"], float)
    config["margin_left"] = input_with_default(
        "   Margen izquierdo", DEFAULTS["margin_left"], float)
    config["margin_right"] = input_with_default(
        "   Margen derecho", DEFAULTS["margin_right"], float)
    config["binding_margin"] = input_with_default(
        "   Margen adicional para encuadernación",
        DEFAULTS["binding_margin"], float)

    # Apply binding margin to left side
    config["margin_left"] += config["binding_margin"]

    # --- Line Appearance ---
    print("\n🎨 APARIENCIA DE LÍNEAS")
    print("-" * 40)
    print("   Color: introduce valor de gris 0-100 (0=negro, 100=blanco)")
    gray_value = input_with_default(
        "   Gris de líneas (75 = gris suave estándar)", 75, float) / 100
    config["line_color_rgb"] = (gray_value, gray_value, gray_value)
    config["line_weight"] = input_with_default(
        "   Grosor de línea en puntos (0.3 = fino)",
        DEFAULTS["line_weight"], float)

    # --- Pagination ---
    print("\n📖 PAGINACIÓN")
    print("-" * 40)
    config["pages"] = input_with_default(
        "   Número total de páginas (múltiplo de 4 para cuadernillos)",
        DEFAULTS["pages"], int)

    print("   Páginas por hoja:")
    print("     1 = Una página por hoja")
    print("     2 = Dos páginas lado a lado (para doblar)")
    print("     4 = Cuatro páginas (imposición para cuadernillo)")
    config["pages_per_sheet"] = input_with_default(
        "   Páginas por hoja", DEFAULTS["pages_per_sheet"], int)
    if config["pages_per_sheet"] not in [1, 2, 4]:
        print("   ⚠ Valor inválido, usando 1")
        config["pages_per_sheet"] = 1

    config["page_numbers"] = input_yes_no(
        "   ¿Incluir números de página?", DEFAULTS["page_numbers"])

    # --- Additional Options ---
    print("\n⚙️  OPCIONES ADICIONALES")
    print("-" * 40)
    print("   Perforaciones: none, 2-hole, 4-hole")
    config["punch_holes"] = input_with_default(
        "   Guías de perforación", DEFAULTS["punch_holes"])

    config["bleed"] = input_with_default(
        "   Sangrado para impresión profesional en mm (0 = sin sangrado)",
        DEFAULTS["bleed"], float)

    # --- Filename ---
    print("\n💾 ARCHIVO")
    print("-" * 40)
    default_filename = (
        f"cuaderno_{config['pattern']}_{config['page_size']}_"
        f"{config['pages']}pag.pdf"
    )
    filename = input_with_default("   Nombre del archivo", default_filename)
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    return filename, config


def quick_mode():
    """Quick generation with all defaults."""
    print("\n🚀 Modo rápido: generando con valores por defecto españoles...")
    config = DEFAULTS.copy()
    config["margin_left"] += config["binding_margin"]
    filename = f"cuaderno_{config['pattern']}_{config['page_size']}_{config['pages']}pag.pdf"
    return filename, config


def main():
    """Main entry point."""
    print("\n" + "=" * 60)
    print("📓 GENERADOR DE CUADERNOS PDF")
    print("   Para encuadernación artesanal")
    print("=" * 60)

    mode = input("\n¿Modo rápido con defaults? (s/n) [n]: ").strip().lower()

    if mode in ["s", "si", "sí", "y", "yes"]:
        filename, config = quick_mode()
    else:
        filename, config = get_user_config()

    print("\n⏳ Generando PDF...")
    create_notebook_pdf(filename, config)

    print("\n" + "=" * 60)
    print("📋 RESUMEN DE CONFIGURACIÓN:")
    print("-" * 40)
    print(f"   Tamaño: {config['page_size'].upper()}")
    print(f"   Orientación: {config['orientation']}")
    print(f"   Patrón: {config['pattern']}")
    print(f"   Páginas: {config['pages']}")
    print(f"   Páginas/hoja: {config['pages_per_sheet']}")
    print(f"   Márgenes: {config['margin_top']}/{config['margin_right']}/"
          f"{config['margin_bottom']}/{config['margin_left']} mm")
    print("=" * 60)


if __name__ == "__main__":
    main()

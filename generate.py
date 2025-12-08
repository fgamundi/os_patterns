#!/usr/bin/env python3
"""
Enhanced Notebook PDF Generator with Terminal UI
Generates customizable notebook pages for handmade bookbinding.
Defaults follow Spanish handmade notebook industry standards.
"""

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, OptionList, Button, Footer, Header, Label
from textual.widgets.option_list import Option
from textual.binding import Binding
from textual import on

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

# Configuration schema with options and descriptions
CONFIG_SCHEMA = {
    "page_size": {
        "label": "Tamaño de página",
        "type": "choice",
        "options": {
            "a5": {"label": "A5 (148×210mm)", "desc": "El más popular para cuadernos artesanales. Tamaño compacto ideal para llevar."},
            "a4": {"label": "A4 (210×297mm)", "desc": "Tamaño estándar de folio. Ideal para cuadernos de escritorio."},
            "a6": {"label": "A6 (105×148mm)", "desc": "Tamaño bolsillo. Perfecto para libretas de notas rápidas."},
            "b5": {"label": "B5 (176×250mm)", "desc": "Intermedio entre A4 y A5. Popular en Japón y Corea."},
            "letter": {"label": "Letter (216×279mm)", "desc": "Estándar estadounidense. Similar al A4."},
        },
        "default": "a5",
    },
    "orientation": {
        "label": "Orientación",
        "type": "choice",
        "options": {
            "portrait": {"label": "Vertical (Portrait)", "desc": "Orientación clásica de cuaderno. La más común para escritura."},
            "landscape": {"label": "Horizontal (Landscape)", "desc": "Orientación apaisada. Ideal para dibujo y storyboards."},
        },
        "default": "portrait",
    },
    "pattern": {
        "label": "Patrón",
        "type": "choice",
        "options": {
            "squared": {"label": "Cuadrícula", "desc": "Patrón de cuadrados. El más versátil, muy popular en España."},
            "lined": {"label": "Líneas", "desc": "Líneas horizontales para escritura. Pauta tradicional española."},
            "dotted": {"label": "Puntos", "desc": "Rejilla de puntos. Popular para bullet journal y lettering."},
            "blank": {"label": "En blanco", "desc": "Sin patrón. Para dibujo libre y bocetos."},
            "cornell": {"label": "Cornell", "desc": "Método de notas Cornell. Con columna de conceptos y resumen."},
            "isometric": {"label": "Isométrico", "desc": "Rejilla isométrica a 30°. Para dibujo técnico y 3D."},
            "hexagonal": {"label": "Hexagonal", "desc": "Patrón de hexágonos. Para química y diseño de juegos."},
        },
        "default": "squared",
    },
    "spacing": {
        "label": "Espaciado (mm)",
        "type": "choice",
        "options": {
            "4": {"label": "4 mm", "desc": "Espaciado fino. Ideal para letra pequeña o cálculos."},
            "5": {"label": "5 mm", "desc": "Estándar español para cuadrícula. El más común."},
            "6": {"label": "6 mm", "desc": "Espaciado medio. Bueno para escritura normal."},
            "7": {"label": "7 mm", "desc": "Espaciado amplio. Cómodo para notas rápidas."},
            "8": {"label": "8 mm", "desc": "Pauta española estándar para líneas. Tradicional."},
            "10": {"label": "10 mm", "desc": "Espaciado muy amplio. Para caligrafía o letra grande."},
        },
        "default": "5",
    },
    "margin_top": {
        "label": "Margen superior (mm)",
        "type": "choice",
        "options": {
            "5": {"label": "5 mm", "desc": "Margen mínimo. Maximiza el área de escritura."},
            "10": {"label": "10 mm", "desc": "Margen estándar. Balance entre espacio y área útil."},
            "15": {"label": "15 mm", "desc": "Margen amplio. Deja espacio para encabezados."},
            "20": {"label": "20 mm", "desc": "Margen muy amplio. Aspecto más elegante."},
        },
        "default": "10",
    },
    "margin_bottom": {
        "label": "Margen inferior (mm)",
        "type": "choice",
        "options": {
            "5": {"label": "5 mm", "desc": "Margen mínimo."},
            "10": {"label": "10 mm", "desc": "Margen estándar."},
            "15": {"label": "15 mm", "desc": "Margen amplio."},
            "20": {"label": "20 mm", "desc": "Margen muy amplio."},
        },
        "default": "10",
    },
    "margin_left": {
        "label": "Margen izquierdo (mm)",
        "type": "choice",
        "options": {
            "5": {"label": "5 mm", "desc": "Margen mínimo."},
            "10": {"label": "10 mm", "desc": "Margen estándar."},
            "15": {"label": "15 mm", "desc": "Margen amplio. Recomendado para encuadernación."},
            "20": {"label": "20 mm", "desc": "Margen muy amplio. Para encuadernación cosida."},
        },
        "default": "15",
    },
    "margin_right": {
        "label": "Margen derecho (mm)",
        "type": "choice",
        "options": {
            "5": {"label": "5 mm", "desc": "Margen mínimo."},
            "10": {"label": "10 mm", "desc": "Margen estándar."},
            "15": {"label": "15 mm", "desc": "Margen amplio."},
            "20": {"label": "20 mm", "desc": "Margen muy amplio."},
        },
        "default": "10",
    },
    "line_gray": {
        "label": "Color de línea (gris %)",
        "type": "choice",
        "options": {
            "50": {"label": "50% - Gris medio", "desc": "Líneas bien visibles. Para uso con lápiz."},
            "65": {"label": "65% - Gris claro", "desc": "Buen contraste. Visibles pero no dominantes."},
            "75": {"label": "75% - Gris suave", "desc": "Estándar español. Discretas pero visibles."},
            "85": {"label": "85% - Gris muy claro", "desc": "Muy sutiles. Las líneas no compiten con la escritura."},
        },
        "default": "75",
    },
    "line_weight": {
        "label": "Grosor de línea (pt)",
        "type": "choice",
        "options": {
            "0.2": {"label": "0.2 pt - Ultrafino", "desc": "Líneas muy delicadas. Para papel de alta calidad."},
            "0.3": {"label": "0.3 pt - Fino", "desc": "Estándar para cuadernos de calidad."},
            "0.4": {"label": "0.4 pt - Normal", "desc": "Grosor medio. Buena visibilidad."},
            "0.5": {"label": "0.5 pt - Grueso", "desc": "Líneas más marcadas. Para patrones grandes."},
        },
        "default": "0.3",
    },
    "pages": {
        "label": "Número de páginas",
        "type": "choice",
        "options": {
            "8": {"label": "8 páginas", "desc": "Cuadernillo simple. Un solo pliego A4 doblado."},
            "16": {"label": "16 páginas", "desc": "Dos pliegos. Libreta pequeña."},
            "32": {"label": "32 páginas", "desc": "Estándar para cuadernillos. Signature común."},
            "48": {"label": "48 páginas", "desc": "Tres signatures. Cuaderno mediano."},
            "64": {"label": "64 páginas", "desc": "Cuatro signatures. Cuaderno completo."},
            "96": {"label": "96 páginas", "desc": "Seis signatures. Cuaderno grueso."},
            "128": {"label": "128 páginas", "desc": "Ocho signatures. Diario o journal."},
        },
        "default": "32",
    },
    "pages_per_sheet": {
        "label": "Páginas por hoja",
        "type": "choice",
        "options": {
            "1": {"label": "1 página/hoja", "desc": "Una página por hoja. Sin imposición."},
            "2": {"label": "2 páginas/hoja", "desc": "Dos páginas lado a lado. Para doblar por la mitad."},
            "4": {"label": "4 páginas/hoja", "desc": "Imposición para cuadernillo. Saddle-stitch."},
        },
        "default": "1",
    },
    "header_line": {
        "label": "Línea de encabezado",
        "type": "choice",
        "options": {
            "no": {"label": "Sin encabezado", "desc": "Patrón uniforme en toda la página."},
            "yes": {"label": "Con encabezado", "desc": "Línea superior destacada para título/fecha."},
        },
        "default": "no",
    },
    "page_numbers": {
        "label": "Números de página",
        "type": "choice",
        "options": {
            "no": {"label": "Sin numerar", "desc": "Páginas sin número. Aspecto más limpio."},
            "yes": {"label": "Numeradas", "desc": "Incluye número de página. Útil para índices."},
        },
        "default": "no",
    },
    "punch_holes": {
        "label": "Guías de perforación",
        "type": "choice",
        "options": {
            "none": {"label": "Sin perforación", "desc": "Sin guías de agujeros."},
            "2-hole": {"label": "2 agujeros", "desc": "Perforación estándar de 2 agujeros (80mm)."},
            "4-hole": {"label": "4 agujeros", "desc": "Perforación europea de 4 agujeros."},
        },
        "default": "none",
    },
}

# =============================================================================
# PDF GENERATION FUNCTIONS (same as before)
# =============================================================================

def get_pagesize(choice, orientation):
    """Get page dimensions based on size choice and orientation."""
    size = PAGE_SIZES.get(choice.lower(), A5)
    if orientation == "landscape":
        return landscape(size)
    return portrait(size)


def parse_color(gray_value):
    """Convert gray percentage to ReportLab Color."""
    g = float(gray_value) / 100
    return Color(g, g, g)


def draw_lined(c, x_start, y_start, width, height, config):
    """Draw horizontal lines (pauta)."""
    spacing = float(config["spacing"]) * mm
    margin_top = float(config["margin_top"]) * mm
    margin_bottom = float(config["margin_bottom"]) * mm
    margin_left = float(config["margin_left"]) * mm
    margin_right = float(config["margin_right"]) * mm

    if config["header_line"] == "yes":
        header_y = y_start + height - margin_top
        c.setStrokeColor(parse_color(config["line_gray"]))
        c.setLineWidth(float(config["line_weight"]) * 1.5)
        c.line(x_start + margin_left, header_y,
               x_start + width - margin_right, header_y)
        c.setLineWidth(float(config["line_weight"]))
        start_y = header_y - spacing * 2
    else:
        start_y = y_start + height - margin_top - spacing

    y = start_y
    while y > y_start + margin_bottom:
        c.line(x_start + margin_left, y, x_start + width - margin_right, y)
        y -= spacing


def draw_dotted(c, x_start, y_start, width, height, config):
    """Draw dot grid (punteado)."""
    spacing = float(config["spacing"]) * mm
    margin_top = float(config["margin_top"]) * mm
    margin_bottom = float(config["margin_bottom"]) * mm
    margin_left = float(config["margin_left"]) * mm
    margin_right = float(config["margin_right"]) * mm
    dot_radius = float(config["line_weight"]) * 0.6

    c.setFillColor(parse_color(config["line_gray"]))

    y = y_start + height - margin_top
    while y > y_start + margin_bottom:
        x = x_start + margin_left
        while x < x_start + width - margin_right:
            c.circle(x, y, dot_radius, fill=1, stroke=0)
            x += spacing
        y -= spacing


def draw_squared(c, x_start, y_start, width, height, config):
    """Draw grid/graph paper (cuadrícula)."""
    spacing = float(config["spacing"]) * mm
    margin_top = float(config["margin_top"]) * mm
    margin_bottom = float(config["margin_bottom"]) * mm
    margin_left = float(config["margin_left"]) * mm
    margin_right = float(config["margin_right"]) * mm

    left = x_start + margin_left
    right = x_start + width - margin_right
    top = y_start + height - margin_top
    bottom = y_start + margin_bottom

    x = left
    while x <= right:
        c.line(x, bottom, x, top)
        x += spacing

    y = bottom
    while y <= top:
        c.line(left, y, right, y)
        y += spacing


def draw_cornell(c, x_start, y_start, width, height, config):
    """Draw Cornell note-taking layout."""
    margin = float(config["margin_left"]) * mm
    line_spacing = float(config["spacing"]) * mm

    cue_column_width = width * 0.25
    summary_height = height * 0.15

    c.setStrokeColor(parse_color(config["line_gray"]))
    c.setLineWidth(float(config["line_weight"]) * 2)

    cue_x = x_start + cue_column_width
    c.line(cue_x, y_start + summary_height, cue_x, y_start + height - margin)
    c.line(x_start + margin, y_start + summary_height,
           x_start + width - margin, y_start + summary_height)

    c.setLineWidth(float(config["line_weight"]))
    y = y_start + height - margin - line_spacing
    while y > y_start + summary_height + margin:
        c.line(cue_x + margin/2, y, x_start + width - margin, y)
        y -= line_spacing


def draw_isometric(c, x_start, y_start, width, height, config):
    """Draw isometric grid for technical drawing."""
    spacing = float(config["spacing"]) * mm
    margin = float(config["margin_left"]) * mm

    left = x_start + margin
    right = x_start + width - margin
    top = y_start + height - margin
    bottom = y_start + margin

    angle = math.radians(30)
    dx = spacing
    dy = spacing * math.tan(angle)

    c.setStrokeColor(parse_color(config["line_gray"]))
    c.setLineWidth(float(config["line_weight"]))

    y = bottom
    while y <= top:
        c.line(left, y, right, y)
        y += dy * 2

    x = left
    while x <= right + (top - bottom) / math.tan(angle):
        x1, y1 = x, bottom
        x2 = x - (top - bottom) / math.tan(angle)
        y2 = top
        if x2 < left:
            y2 = bottom + (x - left) * math.tan(angle)
            x2 = left
        if x1 > right:
            y1 = bottom + (x - right) * math.tan(angle)
            x1 = right
        if y1 >= bottom and y2 <= top:
            c.line(x1, y1, x2, y2)
        x += dx

    x = left - (top - bottom) / math.tan(angle)
    while x <= right:
        x1, y1 = x, bottom
        x2 = x + (top - bottom) / math.tan(angle)
        y2 = top
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
    size = float(config["spacing"]) * mm
    margin = float(config["margin_left"]) * mm

    c.setStrokeColor(parse_color(config["line_gray"]))
    c.setLineWidth(float(config["line_weight"]))

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

    c.setStrokeColor(parse_color(config["line_gray"]))
    c.setLineWidth(float(config["line_weight"]))

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


def draw_page_number(c, page_width, page_height, page_num, config):
    """Draw page number."""
    c.setFillColor(Color(0.5, 0.5, 0.5))
    c.setFont("Helvetica", 8)
    margin = float(config["margin_bottom"]) * mm

    if page_num % 2 == 0:
        x = float(config["margin_left"]) * mm
    else:
        x = page_width - float(config["margin_right"]) * mm

    c.drawString(x, margin / 2, str(page_num))


def draw_punch_holes(c, page_width, page_height, hole_type, margin):
    """Draw punch hole guides."""
    if hole_type == "none":
        return

    c.setStrokeColor(Color(0.8, 0.8, 0.8))
    c.setLineWidth(0.5)

    hole_radius = 3 * mm
    x = margin / 2

    if hole_type == "2-hole":
        center_y = page_height / 2
        positions = [center_y - 40*mm, center_y + 40*mm]
    elif hole_type == "4-hole":
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


def create_imposed_page(c, sheet_width, sheet_height, pages_per_sheet,
                        start_page, config):
    """Create an imposed sheet with multiple pages."""
    pages_per_sheet = int(pages_per_sheet)

    if pages_per_sheet == 1:
        draw_pattern(c, 0, 0, sheet_width, sheet_height, config)
        if config["page_numbers"] == "yes" and start_page > 0:
            draw_page_number(c, sheet_width, sheet_height, start_page, config)
        if config["punch_holes"] != "none":
            draw_punch_holes(c, sheet_width, sheet_height,
                           config["punch_holes"], float(config["margin_left"]) * mm)

    elif pages_per_sheet == 2:
        half_width = sheet_width / 2

        draw_pattern(c, 0, 0, half_width, sheet_height, config)
        if config["page_numbers"] == "yes" and start_page > 0:
            draw_page_number(c, half_width, sheet_height, start_page, config)

        draw_pattern(c, half_width, 0, half_width, sheet_height, config)
        if config["page_numbers"] == "yes" and start_page > 0:
            draw_page_number(c, half_width, sheet_height, start_page + 1, config)

        c.setStrokeColor(Color(0.9, 0.9, 0.9))
        c.setLineWidth(0.2)
        c.setDash(3, 3)
        c.line(half_width, 0, half_width, sheet_height)
        c.setDash()

    elif pages_per_sheet == 4:
        half_width = sheet_width / 2
        half_height = sheet_height / 2

        draw_pattern(c, 0, half_height, half_width, half_height, config)
        draw_pattern(c, half_width, half_height, half_width, half_height, config)
        draw_pattern(c, 0, 0, half_width, half_height, config)
        draw_pattern(c, half_width, 0, half_width, half_height, config)

        c.setStrokeColor(Color(0.9, 0.9, 0.9))
        c.setLineWidth(0.2)
        c.setDash(3, 3)
        c.line(half_width, 0, half_width, sheet_height)
        c.line(0, half_height, sheet_width, half_height)
        c.setDash()


def create_notebook_pdf(filename, config):
    """Create the notebook PDF with all configured options."""
    page_width, page_height = get_pagesize(config["page_size"],
                                            config["orientation"])

    c = canvas.Canvas(filename, pagesize=(page_width, page_height))

    total_pages = int(config["pages"])
    pages_per_sheet = int(config["pages_per_sheet"])
    sheets_needed = math.ceil(total_pages / pages_per_sheet)

    for sheet in range(sheets_needed):
        start_page = sheet * pages_per_sheet + 1
        create_imposed_page(c, page_width, page_height, pages_per_sheet,
                          start_page, config)
        c.showPage()

    c.save()
    return sheets_needed


# =============================================================================
# TEXTUAL TUI APPLICATION
# =============================================================================

class NotebookGeneratorApp(App):
    """Main TUI Application for notebook PDF generation."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 3;
        grid-columns: 1fr 1fr;
        grid-rows: auto 1fr auto;
    }

    Header {
        column-span: 2;
    }

    #settings-container {
        border: solid $primary;
        border-title-color: $text;
        border-title-style: bold;
        height: 100%;
    }

    #options-container {
        border: solid $secondary;
        border-title-color: $text;
        border-title-style: bold;
        height: 100%;
    }

    #settings-list {
        height: 100%;
        scrollbar-size: 1 1;
    }

    #options-list {
        height: 100%;
        scrollbar-size: 1 1;
    }

    #bottom-panel {
        column-span: 2;
        height: auto;
        max-height: 8;
        border: solid $surface;
        padding: 1;
    }

    #description {
        height: auto;
        padding: 0 1;
    }

    #buttons {
        height: auto;
        align: center middle;
        padding-top: 1;
    }

    Button {
        margin: 0 2;
        min-width: 16;
        height: 3;
    }

    #generate-btn {
        background: $success;
        color: $text;
    }

    #quit-btn {
        background: $error;
        color: $text;
    }
    """

    BINDINGS = [
        Binding("tab", "switch_panel", "Cambiar panel"),
        Binding("shift+tab", "switch_panel", "Cambiar panel"),
        Binding("enter", "select_option", "Seleccionar", show=False),
        Binding("g", "generate", "Generar PDF", show=True),
        Binding("q", "quit", "Salir", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.config = {key: schema["default"] for key, schema in CONFIG_SCHEMA.items()}
        self.current_setting = list(CONFIG_SCHEMA.keys())[0]
        self.active_panel = "settings"
        # Store mapping from list index to keys
        self.setting_keys = list(CONFIG_SCHEMA.keys())
        self.option_keys = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)

        with Vertical(id="settings-container") as container:
            container.border_title = "Configuracion"
            yield OptionList(id="settings-list")

        with Vertical(id="options-container") as container:
            container.border_title = "Opciones"
            yield OptionList(id="options-list")

        with Vertical(id="bottom-panel"):
            yield Label(id="description")
            with Horizontal(id="buttons"):
                yield Button("Generar PDF", id="generate-btn", variant="success")
                yield Button("Salir", id="quit-btn", variant="error")

        yield Footer()

    def on_mount(self) -> None:
        """Initialize the UI when mounted."""
        self.title = "Generador de Cuadernos PDF"
        self.sub_title = "Encuadernacion artesanal"
        self.refresh_settings_list()
        self.refresh_options_list()
        self.query_one("#settings-list", OptionList).focus()

    def refresh_settings_list(self) -> None:
        """Refresh the settings list with current values."""
        settings_list = self.query_one("#settings-list", OptionList)
        settings_list.clear_options()

        for key, schema in CONFIG_SCHEMA.items():
            opt = schema["options"].get(self.config[key], {})
            value_label = opt.get("label", self.config[key])
            label_text = f"{schema['label']}: {value_label}"
            settings_list.add_option(Option(label_text, id=key))

        # Highlight current setting
        for i, key in enumerate(CONFIG_SCHEMA.keys()):
            if key == self.current_setting:
                settings_list.highlighted = i
                break

    def refresh_options_list(self) -> None:
        """Refresh the options list for current setting."""
        options_list = self.query_one("#options-list", OptionList)
        options_list.clear_options()

        schema = CONFIG_SCHEMA[self.current_setting]
        current_value = self.config[self.current_setting]
        self.option_keys = list(schema["options"].keys())

        for i, (key, opt) in enumerate(schema["options"].items()):
            marker = "> " if key == current_value else "  "
            options_list.add_option(Option(f"{marker}{opt['label']}", id=key))
            if key == current_value:
                options_list.highlighted = i

        self.update_description()

    def update_description(self) -> None:
        """Update the description panel."""
        schema = CONFIG_SCHEMA[self.current_setting]
        description = self.query_one("#description", Label)

        options_list = self.query_one("#options-list", OptionList)
        highlighted = options_list.highlighted
        if highlighted is not None and highlighted < len(self.option_keys):
            option_key = self.option_keys[highlighted]
            opt = schema["options"].get(option_key, {})
            desc_text = opt.get("desc", "")
            description.update(f"{schema['label']}\n{desc_text}")
        else:
            description.update(f"{schema['label']}")

    @on(OptionList.OptionHighlighted, "#settings-list")
    def on_setting_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        """Handle setting selection change."""
        if event.option and event.option.id:
            self.current_setting = str(event.option.id)
            self.refresh_options_list()

    @on(OptionList.OptionHighlighted, "#options-list")
    def on_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        """Handle option highlight change."""
        self.update_description()

    @on(OptionList.OptionSelected, "#options-list")
    def on_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection."""
        if event.option and event.option.id:
            option_key = str(event.option.id)
            self.config[self.current_setting] = option_key
            schema = CONFIG_SCHEMA[self.current_setting]
            option_label = schema["options"][option_key]["label"]
            self.refresh_settings_list()
            self.refresh_options_list()
            self.notify(f"{schema['label']}: {option_label}")

    @on(Button.Pressed, "#generate-btn")
    def on_generate_pressed(self) -> None:
        """Handle generate button press."""
        self.action_generate()

    @on(Button.Pressed, "#quit-btn")
    def on_quit_pressed(self) -> None:
        """Handle quit button press."""
        self.exit()

    def action_switch_panel(self) -> None:
        """Switch focus between settings and options panels."""
        if self.active_panel == "settings":
            self.query_one("#options-list", OptionList).focus()
            self.active_panel = "options"
        else:
            self.query_one("#settings-list", OptionList).focus()
            self.active_panel = "settings"

    def action_select_option(self) -> None:
        """Select the currently highlighted option."""
        if self.active_panel == "options":
            options_list = self.query_one("#options-list", OptionList)
            highlighted = options_list.highlighted
            if highlighted is not None and highlighted < len(self.option_keys):
                option_key = self.option_keys[highlighted]
                self.config[self.current_setting] = option_key
                self.refresh_settings_list()
                self.refresh_options_list()
                self.notify("Actualizado")

    def action_generate(self) -> None:
        """Generate the PDF."""
        filename = f"cuaderno_{self.config['pattern']}_{self.config['page_size']}_{self.config['pages']}pag.pdf"

        try:
            sheets = create_notebook_pdf(filename, self.config)
            self.notify(
                f"PDF creado: {filename} ({sheets} hojas)",
                severity="information",
                timeout=5
            )
        except Exception as e:
            self.notify(f"Error: {str(e)}", severity="error", timeout=5)


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point."""
    app = NotebookGeneratorApp()
    app.run()


if __name__ == "__main__":
    main()

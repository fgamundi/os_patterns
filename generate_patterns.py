from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A5, landscape, portrait
from reportlab.lib.units import mm

# --- Utility Functions ---

def get_pagesize(choice, orientation):
    if choice == "a4":
        size = A4
    elif choice == "a5":
        size = A5
    else:
        print("Unknown size, defaulting to A4")
        size = A4

    if orientation == "landscape":
        return landscape(size)
    else:
        return portrait(size)

# --- Drawing Functions ---

def draw_lined(c, page_width, page_height, spacing, margin):
    """Standard lined page"""
    y = page_height - margin - spacing
    while y > margin:
        c.line(margin, y, page_width - margin, y)
        y -= spacing

def draw_dotted(c, page_width, page_height, spacing, margin):
    """Dotted page"""
    y = page_height - margin
    while y > margin:
        x = margin
        while x < page_width - margin:
            c.circle(x, y, 0.4, fill=1)
            x += spacing
        y -= spacing

def draw_squared(c, page_width, page_height, spacing, margin):
    """Squared (graph) page"""
    # Vertical lines
    x = margin
    while x < page_width - margin:
        c.line(x, margin, x, page_height - margin)
        x += spacing
    # Horizontal lines
    y = margin
    while y < page_height - margin:
        c.line(margin, y, page_width - margin, y)
        y += spacing

def draw_lined_split(c, page_width, page_height, spacing, margin, corner_radius=5*mm):
    """Split lined version with 2 rounded boxes, respecting margins properly."""
    half_width = page_width / 2
    
    box_width = half_width - 2 * margin
    box_height = page_height - 2 * margin

    # Left and right box lower-left coordinates
    left_x, left_y = margin, margin
    right_x, right_y = half_width + margin, margin

    # Draw rounded rectangles
    # c.roundRect(left_x, left_y, box_width, box_height, corner_radius)
    # c.roundRect(right_x, right_y, box_width, box_height, corner_radius)

    # ---------- Draw LEFT lines ----------
    y = left_y + box_height - margin   # Top margin inside the box
    while y - spacing > left_y + margin:  # Stop before bottom margin
        y -= spacing
        c.line(left_x + margin, y, left_x + box_width - margin, y)

    # ---------- Draw RIGHT lines ----------
    y = right_y + box_height - margin
    while y - spacing > right_y + margin:
        y -= spacing
        c.line(right_x + margin, y, right_x + box_width - margin, y)

# --- Main PDF Creator ---

def create_pattern_pdf(filename, pagesize, pattern, orientation, spacing, margin, split):
    page_width, page_height = get_pagesize(pagesize, orientation)

    c = canvas.Canvas(filename, pagesize=(page_width, page_height))

    if pattern == "lined":
        if split:
            draw_lined_split(c, page_width, page_height, spacing, margin)
        else:
            draw_lined(c, page_width, page_height, spacing, margin)
    elif pattern == "dotted":
        draw_dotted(c, page_width, page_height, spacing, margin)
    elif pattern == "squared":
        draw_squared(c, page_width, page_height, spacing, margin)
    else:
        raise ValueError("Unknown pattern")

    c.showPage()
    c.save()
    print(f"{filename} created.")

# --- Interactive Part ---

def main():
    print("📓 Notebook PDF Generator")
    pagesize = input("Choose page size (A4/Letter) [A4]: ").strip().lower() or "a4"
    pattern = input("Choose pattern (lined/dotted/squared) [lined]: ").strip().lower() or "lined"
    orientation = input("Orientation (portrait/landscape) [landscape]: ").strip().lower() or "landscape"
    split_input = input("Split into two columns (yes/no) [no]: ").strip().lower() or "no"
    split = (split_input in ["yes", "y", "true", "1"])
    margin = input("Page margin in mm [5]: ").strip() or "5"
    margin = float(margin) * mm

    # Ask specific spacing depending on pattern
    if pattern == "lined":
        spacing = input("Line spacing in mm [7]: ").strip() or "7"
    elif pattern == "dotted":
        spacing = input("Dot separation in mm [5]: ").strip() or "5"
    elif pattern == "squared":
        spacing = input("Square size in mm [5]: ").strip() or "5"
    else:
        spacing = "7"

    spacing = float(spacing) * mm

    filename = f"{pattern}_{pagesize}_{orientation}{'_split' if split else ''}.pdf"

    create_pattern_pdf(filename, pagesize, pattern, orientation, spacing, margin, split)


if __name__ == "__main__":
    main()

from PIL import Image, ImageDraw, ImageFont
import random

OUTPUT_SIZE = (1600, 900)

BACKGROUND_COLOR = (5, 8, 15)
TEXT_COLOR = (235, 240, 250)
SECONDARY_TEXT_COLOR = (150, 165, 185)
ACCENT_COLOR = (100, 180, 255)

def load_fonts():
    title = ImageFont.truetype(
        "Nexium.ttf",
        52
    )

    subtitle = ImageFont.truetype(
        "Nexium.ttf",
        40
    )

    label = ImageFont.truetype(
        "Nexium.ttf",
        30
    )

    value = ImageFont.truetype(
        "Nexium.ttf",
        32
    )

    return title, subtitle, label, value

def create_background(size):
    image = Image.new(
        "RGBA",
        size,
        BACKGROUND_COLOR
    )

    draw = ImageDraw.Draw(image)

    width, height = size

    random.seed(42)

    for _ in range(400):

        x = random.randrange(width)
        y = random.randrange(height)

        brightness = random.randrange(
            80,
            230
        )

        radius = random.choice([
            1,
            1,
            1,
            2
        ])

        color = (
            brightness,
            brightness,
            brightness
        )

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius
            ),
            fill=color
        )

    return image

def format_value(value, unit=""):
    """
    Format a numeric value for display.
    """

    if value is None:
        return "Unknown"

    if isinstance(value, float):
        if abs(value) >= 100:
            value = round(value)
        elif abs(value) >= 10:
            value = round(value, 1)
        else:
            value = round(value, 2)

    return f"{value} {unit}".strip()

def draw_planet_info(draw, planet, x, y, fonts):
    """
    Draw planet information at (x, y).
    """

    title_font, subtitle_font, label_font, value_font = fonts

    name = planet.get(
        "pl_name",
        "Unknown Planet"
    )

    hostname = planet.get(
        "hostname",
        "Unknown Star"
    )

    # Title
    draw.text(
        (x, y),
        name,
        font=title_font,
        fill=TEXT_COLOR
    )

    y += 70

    # Host star
    draw.text(
        (x, y),
        f"Orbiting {hostname}",
        font=subtitle_font,
        fill=SECONDARY_TEXT_COLOR
    )

    y += 55

    # Information rows
    information = [
        (
            "System Planets",
            format_value(
                planet.get("sy_pnum"),
            )
        ),
        (
            "Distance",
            format_value(
                planet.get("sy_dist") * 3.26156,
                "LY"
            )
        ),
        (
            "Discovered",
            format_value(
                planet.get("disc_year"),
            )
        ),
        (
            "Radius",
            format_value(
                planet.get("pl_rade"),
                "ER"
            )
        ),
        (
            "Mass",
            format_value(
                planet.get("pl_masse"),
                "EM"
            )
        ),
        (
            "Orbital Period",
            format_value(
                planet.get("pl_orbper"),
                "d"
            )
        ),
        (
            "Orbit Radius",
            format_value(
                planet.get("pl_orbsmax"),
                "AU"
            )
        ),
        (
            "Temperature",
            format_value(
                planet.get("pl_eqt"),
                "K"
            )
        ),
    ]

    row_height = 42

    for label, value in information:

        draw.text(
            (x, y),
            label,
            font=label_font,
            fill=SECONDARY_TEXT_COLOR
        )

        draw.text(
            (x + 270, y),
            value,
            font=value_font,
            fill=TEXT_COLOR
        )

        y += row_height

def create_planet_poster(
    planet,
    planet_image_path,
    output_path,
    size=OUTPUT_SIZE
):
    """
    Create a finished planet information image.
    """

    fonts = load_fonts()

    background = create_background(size)

    # Planet image
    planet_image = Image.open(
        planet_image_path
    ).convert("RGBA")

    # Resize while preserving aspect ratio
    planet_size = 1200

    scale = planet_size / max(
        planet_image.width,
        planet_image.height
    )

    new_size = (
        int(planet_image.width * scale),
        int(planet_image.height * scale)
    )

    planet_image = planet_image.resize(
        new_size,
        Image.Resampling.LANCZOS
    )

    # Position planet
    planet_x = (size[0] - planet_image.height) // 2
    planet_y = (size[1] - planet_image.height) // 2 - 100

    background.alpha_composite(
        planet_image,
        (
            planet_x,
            planet_y
        )
    )

    # Information
    draw = ImageDraw.Draw(background)

    info_x = 50
    info_y = size[1] - 800

    draw_planet_info(
        draw,
        planet,
        info_x,
        info_y,
        fonts
    )

    # Small footer
    footer_font = ImageFont.truetype(
        "Nexium.ttf",
        20
    )

    draw.text(
        (size[0] // 2, size[1] - 100),
        "Visualization based on NASA Exoplanet Archive data",
        font=footer_font,
        fill=(100, 110, 125),
        anchor="mm",
        align="center"
    )

    background.convert("RGB").save(
        output_path,
        "PNG"
    )

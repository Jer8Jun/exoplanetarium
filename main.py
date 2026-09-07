import tap_api
import texture_gen
import renderer
import poster
import base64
import sys
import json
import os
from PIL import Image
import io

ticket_path = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))

planet = tap_api.get_random_planet()
print(f"Chosen planet: {planet.get('pl_name')}")

base = texture_gen.get_base(planet)
details = texture_gen.get_details(planet)
atmosphere = texture_gen.get_atmosphere(planet)

print(f"""Generating planet with properties:
Base: {base.name}
Details: {[detail.name for detail in details]}
""")

renderer.render_planet(
    base=(
        f"textures/base/{base.get_texture()}",
        base.get_tone()
    ),
    details=[
        (
            f"textures/detail/{detail.get_texture()}",
            detail.get_tone()
        ) for detail in details
    ],
    atmosphere_tone=atmosphere.get_tone(),
    output_path=f"{ticket_path}/planet.png"
)

poster.create_planet_poster(
    planet=planet,
    planet_image_path=f"{ticket_path}/planet.png",
    output_path=f"{ticket_path}/wallpaper.jpg",
    size=(1284, 2778)
)

#compress before saving
img = Image.open(f"{ticket_path}/wallpaper.jpg")
#img.thumbnail((1284, 2778), Image.Resampling.LANCZOS)

buffer = io.BytesIO()
img.convert("RGB").save(buffer, format="JPEG", quality=80, optimize=True)

image_b64 = base64.b64encode(buffer.getvalue()).decode("ascii")

with open(f"{ticket_path}/output.json", "w") as f:
    json.dump({
        "image": image_b64
    }, f)
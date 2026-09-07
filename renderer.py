from PIL import Image
import numpy as np

def load_texture(path, tone):
    image = Image.open(path).convert("RGBA")

    rgb = np.array(image)[..., :3].astype(np.float32)
    alpha = np.array(image)[..., 3]

    tone = np.array(tone, dtype=np.float32)
    rgb = rgb * (tone / 255.0)
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    result = np.dstack((rgb, alpha))

    return Image.fromarray(result, "RGBA")

def overlay_texture(base, texture):
    return Image.alpha_composite(base, texture)

def build_planet_texture(base, details):
    base_path, base_tone = base

    texture = load_texture(base_path, base_tone)

    for detail_path, detail_tone in details:
        detail = load_texture(detail_path, detail_tone)

        texture = overlay_texture(texture, detail)

    return texture

def render_sphere(texture, atmosphere_tone, size=768):
    """
    Turn an equirectangular texture into a shaded spherical planet.

    The texture is assumed to be 2:1, e.g. 1024x512.
    """

    texture_array = np.array(texture)
    tex_height, tex_width = texture_array.shape[:2]

    # --------------------------------------------------------
    # Create output coordinate grid
    # --------------------------------------------------------

    y, x = np.mgrid[0:size, 0:size]

    center = (size - 1) / 2
    radius = size * 0.5

    # Normalize x/y coordinates so the planet has radius 1.
    nx = (x - center) / radius
    ny = (y - center) / radius

    # Pixels inside the circular projection of the sphere.
    sphere_mask = (nx * nx + ny * ny) <= 1.0

    # --------------------------------------------------------
    # Allocate output
    # --------------------------------------------------------

    rgb = np.zeros(
        (size, size, 3),
        dtype=np.float32
    )

    alpha = np.zeros(
        (size, size),
        dtype=np.uint8
    )

    # --------------------------------------------------------
    # Only calculate spherical coordinates for valid pixels
    # --------------------------------------------------------

    valid_nx = nx[sphere_mask]
    valid_ny = ny[sphere_mask]

    # Z coordinate of the sphere.
    #
    # Since:
    #
    #   x² + y² + z² = 1
    #
    # we get:
    #
    #   z = sqrt(1 - x² - y²)
    #
    valid_nz = np.sqrt(
        1.0 - valid_nx**2 - valid_ny**2
    )

    # --------------------------------------------------------
    # Convert XYZ coordinates to longitude / latitude
    # --------------------------------------------------------

    longitude = np.arctan2(
        valid_nx,
        valid_nz
    )

    latitude = np.arcsin(
        np.clip(valid_ny, -1.0, 1.0)
    )

    # --------------------------------------------------------
    # Convert longitude/latitude to texture coordinates
    # --------------------------------------------------------

    u = (
        longitude / (2 * np.pi) + 0.5
    ) * (tex_width - 1)

    v = (
        0.5 - latitude / np.pi
    ) * (tex_height - 1)

    # Convert to integer pixel coordinates.
    u = np.clip(
        u,
        0,
        tex_width - 1
    ).astype(np.int32)

    v = np.clip(
        v,
        0,
        tex_height - 1
    ).astype(np.int32)

    # --------------------------------------------------------
    # Sample the texture
    # --------------------------------------------------------

    sampled = texture_array[v, u, :3]

    rgb[sphere_mask] = sampled

    # --------------------------------------------------------
    # Lighting
    # --------------------------------------------------------

    light = np.array([
        -0.45,
        -0.35,
        0.82
    ])

    light /= np.linalg.norm(light)

    # Surface normals
    normals = np.stack([
        valid_nx,
        valid_ny,
        valid_nz
    ], axis=-1)

    diffuse = np.sum(
        normals * light,
        axis=-1
    )

    # Ambient light prevents the night side from being
    # completely black.
    lighting = (
        0.12 +
        0.88 * np.maximum(diffuse, 0)
    )

    rgb[sphere_mask] *= lighting[:, None]

    # --------------------------------------------------------
    # Atmospheric edge
    # --------------------------------------------------------

    edge = 1.0 - valid_nz

    atmosphere = np.clip(
        (edge - 0.45) / 0.55,
        0,
        1
    )

    atmosphere_color = np.array(atmosphere_tone)

    atmosphere_strength = atmosphere * 0.35

    rgb[sphere_mask] = (
        rgb[sphere_mask]
        * (1 - atmosphere_strength[:, None])
        + atmosphere_color
        * atmosphere_strength[:, None]
    )

    # --------------------------------------------------------
    # Alpha
    # --------------------------------------------------------

    alpha[sphere_mask] = 255

    # --------------------------------------------------------
    # Construct final image
    # --------------------------------------------------------

    rgb = np.clip(
        rgb,
        0,
        255
    ).astype(np.uint8)

    result = np.dstack((
        rgb,
        alpha
    ))

    return Image.fromarray(
        result,
        "RGBA"
    )

def render_planet(
    base,
    details,
    atmosphere_tone,
    output_path,
    size=768
):
    """
    Render a complete planet.

    Parameters
    ----------
    base:
        (path, tone)

    details:
        list of (path, tone)

    ring:
        (path, tone)

    output_path:
        Where to save the PNG.

    size:
        Output image dimensions.
    """

    # Build texture
    texture = build_planet_texture(
        base,
        details,
    )

    # Render sphere
    planet = render_sphere(
        texture,
        atmosphere_tone,
        size=size
    )

    planet.save(
        output_path,
        "PNG"
    )
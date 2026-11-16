
from PIL import Image, ImageOps
import base64
from io import BytesIO

INPUT = r"src/assets/logo.jpg"

# Open image
img = Image.open(INPUT).convert("RGB")

# Grayscale
bw = ImageOps.grayscale(img)

# Invert
inverted = ImageOps.invert(bw)

# Remove dark pixels and preserve transparency
rgba = inverted.convert("RGBA")

pixels = rgba.load()

for y in range(rgba.height):
    for x in range(rgba.width):
        r, g, b, a = pixels[x, y]

        # Convert dark pixels to transparent
        if r < 40:
            pixels[x, y] = (255, 255, 255, 0)
        else:
            # Preserve white/gray details
            pixels[x, y] = (255, 255, 255, r)

# Save PNG
rgba.save("logo_bw_inverted.png")

# Save ICO
rgba.save(
    "logo.ico",
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48),
           (64, 64), (128, 128), (256, 256)]
)

# Save SVG with embedded transparent PNG
buffer = BytesIO()
rgba.save(buffer, format="PNG")
encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{img.width}" height="{img.height}"
     viewBox="0 0 {img.width} {img.height}">
    <image width="{img.width}" height="{img.height}"
           href="data:image/png;base64,{encoded}"/>
</svg>'''

with open("logo.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Successfully generated transparent logo files!")

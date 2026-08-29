from PIL import Image

img = Image.open("logo.png")

sizes = [16, 32, 48, 64, 180, 192, 512]

for s in sizes:
    icon = img.resize((s, s), Image.LANCZOS)
    icon.save(f"favicon-{s}x{s}.png")

img.save(
    "favicon.ico",
    sizes=[(16,16),(32,32),(48,48)]
)
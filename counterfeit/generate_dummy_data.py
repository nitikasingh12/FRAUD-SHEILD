import os
import random
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))


def make_image(path, base_color, noise_level, size=(128, 128)):
    img = Image.new("RGB", size, base_color)
    draw = ImageDraw.Draw(img)
    for _ in range(noise_level):
        x1, y1 = random.randint(0, size[0]), random.randint(0, size[1])
        x2, y2 = x1 + random.randint(-15, 15), y1 + random.randint(-15, 15)
        draw.line([(x1, y1), (x2, y2)], fill=tuple(
            max(0, min(255, c + random.randint(-40, 40))) for c in base_color
        ), width=1)
    img.save(path)


def generate_set(folder, base_color, noise_level, count):
    os.makedirs(folder, exist_ok=True)
    for i in range(count):
        make_image(os.path.join(folder, f"img_{i}.png"), base_color, noise_level)


if __name__ == "__main__":
    generate_set(os.path.join(BASE, "data/train/real"), (150, 180, 140), 25, 40)
    generate_set(os.path.join(BASE, "data/val/real"), (150, 180, 140), 25, 10)
    generate_set(os.path.join(BASE, "data/train/fake"), (170, 165, 120), 8, 40)
    generate_set(os.path.join(BASE, "data/val/fake"), (170, 165, 120), 8, 10)
    print("Synthetic placeholder dataset generated.")
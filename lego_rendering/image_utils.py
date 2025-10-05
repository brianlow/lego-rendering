import os
from PIL import Image

# Combine PIL images into a grid
# Assumes images are the same size
def grid(images, rows=1, cols=1):
    width = images[0].size[0]
    height = images[0].size[1]

    # Create an empty image with correct size
    total_width = cols * width
    total_height = rows * height
    new_image = Image.new('RGBA', (total_width, total_height))

    # Paste the images
    for i, img in enumerate(images):
        row = i // cols
        col = i % cols
        new_image.paste(img, (col * width, row * height))

    return new_image

def get_default_font():
    if os.name == 'nt':  # Windows
        return 'arial.ttf'
    elif os.name == 'posix':  # Linux or Mac
        return '/Library/Fonts/Arial.ttf'

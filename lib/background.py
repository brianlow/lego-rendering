import random
from PIL import Image, ImageDraw
from lib.colors import random_color_for_pil, hsv2rgb

def save_background_image(color, size, num_shapes, filename):
    img = Image.new('RGB', size, color)
    add_random_shapes(img, num_shapes, int(size[0]/3))
    img.save(filename)

def add_random_shapes(img, num_shapes, max_size):
    draw = ImageDraw.Draw(img)
    width, height = img.size
    base_color = random_color_for_pil()
    for i in range(num_shapes):
        color = (base_color[0] + random.randint(-35, 35), base_color[1] + random.randint(-35, 35), base_color[2] + random.randint(-35, 35))
        shape_type = random.choice(['circle', 'rectangle', 'triangle', 'line'])
        shape_size = random.randint(10, max_size)
        x1 = random.randint(0, width - shape_size)
        y1 = random.randint(0, height - shape_size)
        x2 = x1 + shape_size
        y2 = y1 + shape_size
        if shape_type == 'circle':
            draw.ellipse((x1, y1, x2, y2), fill=color)
        elif shape_type == 'rectangle':
            draw.rectangle((x1, y1, x2, y2), fill=color)
        elif shape_type == 'triangle':
            draw.polygon([(x1, y1), (x2, y1), ((x1+x2)//2, y2)], fill=color)
        elif shape_type == 'line':
          draw.line((x1, y1, x2, y2), width=2, fill=color)

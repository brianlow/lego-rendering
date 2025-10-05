from enum import Enum
from math import radians

class Quality(Enum):
    HIGH = 'high'
    NORMAL = 'normal'
    DRAFT = 'draft'

class LightingStyle(Enum):
    DEFAULT = 'default'
    BRIGHT = 'bright'
    HARD = 'hard'

class Look(Enum):
    NORMAL = 'normal'              # realistic
    INSTRUCTIONS = 'instructions'  # line art

class Material(Enum):
    PLASTIC = 'plastic'
    TRANSPARENT = 'transparent'
    RUBBER = 'rubber'

class Format(Enum):
    PNG = 'PNG'
    JPEG = 'JPEG'

class RenderOptions:
    def __init__(self,
                 image_filename = "renders/test.png", # output filename
                 bounding_box_filename = None, # optionally, output the bounding box in YOLO format
                 width = 224,           # standard Imagenet size
                 height = 224,          # standard Imagenet size
                 quality = Quality.NORMAL,     # trade between speed and quality
                 blender_filename = None,      # optionally save a .blend file to debug the render
                 lighting_style = LightingStyle.DEFAULT, # default, soft, hard
                 light_angle = 210,            # angle of the light rotated around the z-axis, 0 - 360
                 part_color = "#FFFFFF",       # color of the part, hex string
                 material = Material.PLASTIC,
                 part_rotation = (0, 0, 0),    # rotation of the part in degrees, xyz tuple
                 camera_height = 45,           # height of the camera as degrees above the ground plane, 0 - 180
                 zoom = 1.0,                   # 1.0 for part to fill frame, < 1.0 to zoom out, > 1.0 to zoom in
                 look = Look.NORMAL,           # normal (realistic) or instructions (line art)
                 format = Format.PNG,          # PNG = lossless, transparent backgrounds, JPG much smaller
                 ):
        self.width = width
        self.height = height
        self.quality = quality
        self.image_filename = image_filename
        self.bounding_box_filename = bounding_box_filename
        self.blender_filename = blender_filename
        self.lighting_style = lighting_style
        self.light_angle = light_angle
        self.part_color = part_color
        self.material = material
        self.part_rotation = part_rotation
        self.camera_height = camera_height
        self.zoom = zoom
        self.look = look
        self.format = format

    @property
    def draft(self):
        return self.quality == Quality.DRAFT

    @property
    def instructions(self):
        return self.look == Look.INSTRUCTIONS

    @property
    def res_prisms(self):
        return "Standard" if self.draft else "High"

    @property
    def use_logo_studs(self):
        return False if self.draft or self.instructions else True

    @property
    def render_samples(self):
        return 16 if self.draft else 256

    @property
    def part_rotation_radian(self):
        return tuple(map(radians, self.part_rotation))

    @property
    def transparent_background(self):
        return self.instructions

    @property
    def render_width(self):
        return self.width * 2 if self.quality == Quality.HIGH else self.width

    @property
    def render_height(self):
        return self.height * 2 if self.quality == Quality.HIGH else self.height

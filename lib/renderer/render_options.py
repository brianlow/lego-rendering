from enum import Enum
from math import radians

class Quality(Enum):
    NORMAL = 'normal'
    DRAFT = 'draft'

class LightingStyle(Enum):
    DEFAULT = 'default'
    BRIGHT = 'bright'
    HARD = 'hard'

class Look(Enum):
    NORMAL = 'normal'              # realistic
    INSTRUCTIONS = 'instructions'  # line art

class RenderOptions:
    def __init__(self,
                 image_filename,            # output filename
                 render_width = 224,        # standard Imagenet size
                 render_height = 224,       # standard Imagenet size
                 quality = Quality.NORMAL,  # trade between speed and quality
                 blender_filename = None,   # optionally save a .blend file to debug the render
                 lighting_style = LightingStyle.DEFAULT, # default, soft, hard
                 light_angle = 210,         # angle of the light rotated around the z-axis, 0 - 360
                 part_color = (0.788, 0.102, 0.035, 1),        # color of the part, RGBA tuple (0 - 1.0)
                 part_transparent = False,  # True for a transparent part, False for opaque
                 part_rotation = (0, 0, 0), # rotation of the part in degrees, xyz tuple
                 camera_height = 45,        # height of the camera as degrees above the ground plane, 0 - 180
                 zoom = 1.0,                # 1.0 for part to fill frame, < 1.0 to zoom out, > 1.0 to zoom in
                 look = Look.NORMAL         # normal (realistic) or instructions (line art)
                 ):
        self.render_width = render_width
        self.render_height = render_height
        self.quality = quality
        self.image_filename = image_filename
        self.blender_filename = blender_filename
        self.lighting_style = lighting_style
        self.light_angle = light_angle
        self.part_color = part_color
        self.part_transparent = part_transparent
        self.part_rotation = part_rotation
        self.camera_height = camera_height
        self.zoom = zoom
        self.look = look

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
        return False if self.draft else True


    @property
    def render_samples(self):
        return 16 if self.draft else 256

    @property
    def part_rotation_radian(self):
        return tuple(map(radians, self.part_rotation))

    @property
    def transparent_background(self):
        return self.instructions

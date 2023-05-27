import random
from enum import Enum

class RebrickableMaterial:
    def __init__(self, id, ldraw_color_id):
       self.id = id
       self.ldraw_color_id = ldraw_color_id

    @property
    def name(self):
        return self.id

class RebrickableMaterials(Enum):
    Plastic = RebrickableMaterial('Plastic', 0),

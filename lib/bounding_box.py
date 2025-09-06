from PIL import ImageFont
import os
import hashlib
import math


class BoundingBox:
    _font = None

    def __init__(self,
                 x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @classmethod
    def from_yolo(cls, yolo_box):
        return cls(
            x1=int(yolo_box.xyxy[0][0].int()),
            y1=int(yolo_box.xyxy[0][1].int()),
            x2=int(yolo_box.xyxy[0][2].int()),
            y2=int(yolo_box.xyxy[0][3].int())
        )

    @classmethod
    def from_xywh(cls, x, y, w, h):
        return cls(
            x1=x,
            y1=y,
            x2=x+w,
            y2=y+h
        )

    @classmethod
    def from_xyxy(cls, x1, y1, x2, y2):
        return cls(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        )

    # Corners is a 4 element array where each element
    # is a corner [x, y]. This box is most likely a
    # parallelogram, so we will calculate a square box
    # that contains all 4 corners.
    @classmethod
    def from_aruco(cls, corners):
        x1 = min(corners[0][0], corners[1][0], corners[2][0], corners[3][0])
        y1 = min(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
        x2 = max(corners[0][0], corners[1][0], corners[2][0], corners[3][0])
        y2 = max(corners[0][1], corners[1][1], corners[2][1], corners[3][1])
        return cls(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2
        )

    @classmethod
    def font(self):
        if self._font is None:
            font_path = os.path.expanduser('~/Library/Fonts/Arial.ttf')
            self._font = ImageFont.truetype(font_path, size=24)
        return self._font

    # Given a list of boxes, combine any where the centers
    # are within threshold pixels of each other
    @classmethod
    def combine_nearby(cls, boxes, threshold):
        combined_boxes = []
        for box in boxes:
            index = next((i for i, combined_box in enumerate(combined_boxes) if box.is_nearby(combined_box, threshold)), None)
            if index is None:
                combined_boxes.append(box)
            else:
                combined_boxes[index] = combined_boxes[index].combine(box)
        return combined_boxes

    @property
    def x(self):
        return self.x1

    @property
    def y(self):
        return self.y1

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def area(self):
        return self.width * self.height

    @property
    def center(self):
        return (self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2

    def is_touching_frame(self, frame_width, frame_height):
        return self.x1 < 5 or self.y1 < 5 or frame_width - self.x2 < 5 or frame_height - self.y2 < 5

    # Extracts a portion of an image
    def crop(self, image):
        return image.crop((int(self.x1), int(self.y1), int(self.x2), int(self.y2)))

    def draw(self, draw, color='white', width=2):
        coords = ((self.x1, self.y1), (self.x2, self.y2))
        draw.rectangle(coords, outline=color, width=width)

    # Draw a label below the box, colors are a hex string
    def draw_label(self, draw, text, text_color, swatch_color):
        x = self.x1  # bottom left corner of box, top left of label
        y = self.y2
        print(BoundingBox.font())
        text_length = BoundingBox.font().getsize(text)[0]
        draw.rectangle(
            ((x, y), (x+25+text_length+25, y+35)), fill='white')
        draw.rectangle(
            ((x+5, y+5), (x+5+25, y+5+25)), fill=f"#{swatch_color}")
        draw.text(
            (x+5+25+10, y+5), text, fill=text_color, font=BoundingBox.font())

    def move(self, x, y):
        return BoundingBox(
            self.x1 + x,
            self.y1 + y,
            self.x2 + x,
            self.y2 + y
        )

    def distance(self, other):
        return math.sqrt((self.center[0] - other.center[0])**2 + (self.center[1] - other.center[1])**2)

    def is_nearby(self, other, threshold):
        return self.distance(other) < threshold

    def combine(self, other):
        x1 = min(self.x1, other.x1)
        y1 = min(self.y1, other.y1)
        x2 = max(self.x2, other.x2)
        y2 = max(self.y2, other.y2)
        return BoundingBox(x1, y1, x2, y2)

    def grow(self, amount):
        return BoundingBox(
            self.x1 - amount,
            self.y1 - amount,
            self.x2 + amount,
            self.y2 + amount
        )

    # Returns new BoundingBox that is square by lengthing the shorter side
    def square(self):
        max_dim = max(self.width, self.height)
        width_diff = max_dim - self.width
        height_diff = max_dim - self.height

        x1_new = self.x1 - width_diff / 2
        x2_new = x1_new + max_dim
        y1_new = self.y1 - height_diff / 2
        y2_new = y1_new + max_dim

        return BoundingBox(x1_new, y1_new, x2_new, y2_new)

    def hash(self):
        bytes = [self.x1, self.y1, self.x2, self.y2].join(".").encode('utf-8')
        return hashlib.sha256(bytes).hexdigest()[:6]

    # Converts to:
    #   [center_x, center_y, width, height] normalized to 0.0-1.0
    #
    def to_yolo(self, image_width, image_height):
        center_x, center_y = self.center
        return [
            center_x/image_width,
            center_y/image_height,
            self.width/image_width,
            self.height/image_height
        ]

    def __repr__(self):
        return f"BoundingBox({self.x1}, {self.y1}, {self.x2}, {self.y2})"

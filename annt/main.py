
import os
import json
import cv2

KEY_OBJECTS = 'objects'
KEY_TYPE = 'typ'


class Annotation():

    def __init__(self, filename, image, boxes=[]):
        self.filename = filename
        self.image = image
        self.boxes = boxes

    def __repr__(self):
        return self.filename

    def show(self, max_width=500, max_height=500):
        width, height, _ = self.image.shape
        if width/height > max_width/max_height:
            rate = max_width/width
        else:
            rate = max_height/height
        new_width = int(width * rate)
        new_height = int(height * rate)
        resized = cv2.resize(self.image, (new_height, new_width))

        # Resize boxes
        for box in self.boxes:
            x1 = int(box.x * rate)
            y1 = int(box.y * rate)
            x2 = int(box.x * rate + box.w * rate)
            y2 = int(box.y * rate + box.h * rate)
            cv2.rectangle(resized, (x1, y1), (x2, y2), (0, 255, 0))

        cv2.imshow(self.filename, resized)
        cv2.waitKey()

    def __resize(self):
        pass



class Box():

    def __init__(self, tag, iwidth, iheight, x, y, w, h):
        self.tag = tag
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image_width = iwidth
        self.image_height = iheight

    def __repr__(self):
        return f'Box - x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}'

    def __str__(self):
        return f'Box - x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}'

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        prev_bottom = self.y + self.h
        self.y = value
        self.h = prev_bottom - self.y

    @property
    def right(self):
        return self.image_width - self.x - self.w

    @right.setter
    def right(self, value):
        self.w = self.image_width - value - self.x

    @property
    def bottom(self):
        return self.image_height - self.y - self.h

    @bottom.setter
    def bottom(self, value):
        self.h = self.image_height - value - self.y

    @property
    def left(self):
        return self.x 

    @left.setter
    def left(self, value):
        prev_right = self.x + self.w
        self.x = value
        self.w = prev_right - self.x


def load(dir_path):
    if not os.path.isdir(dir_path):
        raise IOError(f'{dir_path} not exists')

    image_dir = os.path.join(dir_path, 'images')
    annt_dir = os.path.join(dir_path, 'annotations')
    
    if not os.path.isdir(image_dir) or not os.path.isdir(annt_dir):
        raise IOError('image dir or annotation dir not exists')

    image_files = os.listdir(image_dir)
    annotation_files = set(os.listdir(annt_dir))

    annotations = []
    for f in image_files:
        annt_file = f.split(".")[0] + ".json"
        if annt_file not in annotation_files:
            continue
        img = load_image(os.path.join(image_dir, f))
        img_height, img_width, _ = img.shape
        ant = load_annotation(os.path.join(annt_dir, annt_file), img_width, img_height)
        ant.filename = f
        ant.image = img
        annotations.append(ant)
    return annotations


def load_image(filepath):
    img = cv2.imread(filepath, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    return img


def load_annotation(filepath, img_width, img_height):
    contents = None
    with open(filepath, 'r') as fp:
        contents = json.load(fp)
    
    if KEY_OBJECTS not in contents:
        return None

    boxes = []
    for obj in contents[KEY_OBJECTS]:
        if obj[KEY_TYPE] == 1:
            # Type Box
            tag = obj["name"]
            x, y, w, h = obj["position"]
            box = Box(tag, img_width, img_height, x, y, w, h)
            boxes.append(box)
    annotation = Annotation(None, None, boxes)
    return annotation


def show(image, objects):
    pass

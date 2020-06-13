
import os
import json
import cv2
from . import color
from . import utils

KEY_OBJECTS = 'objects'
KEY_TYPE = 'typ'
KEY_TAGS = 'tags'

NAME_IMAGES_DIR = 'images'
NAME_ANNOTATION_DIR = 'annotations'
NAME_METAFILE = 'taginfo.json'


class Annotation():

    def __init__(self, filename, image, boxes=[]):
        self.filename = filename
        self.image = image
        self.boxes = boxes
        self.color_map = {}

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
            c = self.color_map.get(box.tag, (0, 0, 0))
            resized = utils.draw_rectangle(resized, (x1, y1), (x2, y2), c, 0.5)
            cv2.rectangle(resized, (x1, y1), (x2, y2), c)

            tag_text = box.tag
            # If tag_text is ascii string, display text
            if len(tag_text) != len(tag_text.encode()):
                continue

            # Adjust text size
            width = abs(x2 - x1)
            font = cv2.FONT_HERSHEY_DUPLEX
            font_size = 0.5
            font_thickness = 1
            color_code = (0, 0, 0)
            shrinked = False

            while cv2.getTextSize(tag_text, font, font_size, font_thickness)[0][0] > width:
                if tag_text == "":
                    break
                tag_text = tag_text[:-1]
                shrinked = True
            if shrinked:
                tag_text += ".."

            cv2.putText(resized, tag_text, (x1, y1), font, font_size, color_code, font_thickness)

        cv2.imshow(self.filename, resized)
        cv2.waitKey()


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
    """ load annotation files.
    """
    if not os.path.isdir(dir_path):
        raise IOError(f'{dir_path} not exists')

    image_dir = os.path.join(dir_path, NAME_IMAGES_DIR)
    annt_dir = os.path.join(dir_path, NAME_ANNOTATION_DIR)
    metapath = os.path.join(dir_path, NAME_METAFILE)
    
    if not os.path.isdir(image_dir) or not os.path.isdir(annt_dir):
        raise IOError('image dir or annotation dir not exists')

    name_ls, cidx_ls = load_meta(metapath)
    name_set = set(name_ls)
    color_map = {}
    for n, ci in zip(name_ls, cidx_ls):
        h = color.idx_to_hue(ci)
        c = color.hsv_to_rgb(h, 1, 0.7)
        # Revser tuple to convert (r, g, b) to (b, g, r)
        c = tuple(reversed(c))
        color_map[n] = c
    del(name_ls)
    del(cidx_ls)

    image_files = os.listdir(image_dir)
    annotation_files = set(os.listdir(annt_dir))

    annotations = []
    for f in image_files:
        annt_file = f.split(".")[0] + ".json"
        if annt_file not in annotation_files:
            continue
        img = load_image(os.path.join(image_dir, f))
        img_height, img_width, _ = img.shape
        ant = load_annotation(os.path.join(annt_dir, annt_file), img_width, img_height, name_set)
        ant.color_map.update(color_map)
        ant.filename = f
        ant.image = img
        annotations.append(ant)
    return annotations


def load_meta(filepath):
    """ Load metafile
    Args:
        filepath(str): Metafile filepath
    Returns:
        (list, list): Pair of tag name list and color index list

    """
    with open(filepath) as fp:
        obj = json.load(fp)

    if not KEY_TAGS in obj.keys():
        raise RuntimeError('invalid format')

    cidx_ls = []
    name_ls = []
    for c in obj[KEY_TAGS]:
        cidx = c['colorIdx']
        name = c['tagName']
        cidx_ls.append(cidx)
        name_ls.append(name)
    return name_ls, cidx_ls
        

def load_image(filepath):
    """ Load image from filepath
    Args:
        filepath(str): Image filepath
    Returns:
        np.ndarray
    """
    img = cv2.imread(filepath, cv2.IMREAD_IGNORE_ORIENTATION | cv2.IMREAD_COLOR)
    return img


def load_annotation(filepath, img_width, img_height, available_tags=None):
    """ Load annotation information from filepath
    Args:
        filepath(str): annotation filepath.
        img_width(int): Image width
        img_height(int): Image height
        available_tags(set, optional): This function read only the tags specified here.
    Returns:
        Annotation
    """
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
            if available_tags is not None and tag not in available_tags:
                continue
            x, y, w, h = obj["position"]
            box = Box(tag, img_width, img_height, x, y, w, h)
            boxes.append(box)
    annotation = Annotation(None, None, boxes)
    return annotation

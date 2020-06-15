annt
====
Simple annotated file loader for object detection task.

## Description
Various tools have been developed so far for object detection tasks.
However, there are no standard in annotation tools and formats and
developers still write their own json or xml parser of annotation files.
'annt' resolve this problem. Once you annotate image on annt webapp,
 you can load annotation images immediately and
focus on the essential AI development.

## Usage and Example
``` python
import annt

# annotations is list of annotation data
annotations = annt.load('~/Dropbox/app/project_name')

# Display ths information of each annotation file.
for a in annotations:
  image = a.image  # opencv2 image array
  boxes = a.boxes  # list of bounding boxes

  height, width, colors = image.shape  # you can

  for box in boxes:
    # Tag information (str)
    print(f'~ tag name : box.tag ~')

    # You can get coordination information of the box by two methods,
    # Left Top Style and Edge Style.
    # Coordination information based on left top of the box. (Left-Top Style)
    print(f'x : {box.x}')
    print(f'y : {box.y}')
    print(f'w : {box.w}')
    print(f'h : {box.h}')

    # Coordination information based on the distance from each edge of the image. (Edge Style)
    print(f'left : {box.left}')
    print(f'right : {box.right}')
    print(f'top : {box.top}')
    print(f'bottom : {box.bottom}'

    # If you change these coordination properties, all of them will recomputed.
    box.w = 300  # This operation will also change box.right property.

```

## Getting Started
1. Register annt and annotate imaes.
2. Install this libary from pip.
3. Develop you own project.

## Install

you can install from pip.
```
pip install annt
```
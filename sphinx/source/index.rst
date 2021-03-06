
============
annt 
============


Description
============
Various tools have been developed so far for object detection tasks.
However, there are no standard in annotation tools and formats and
developers still write their own json or xml parser of annotation files.
`annt <https://annt.ai/>`_ is an annotation tool that operates in the form of cloud services such as dropbox.
annt provides not only simple and comfortable annotation exprience, but also powerful library for loading annotated images.

This is a documentation for `python library <https://github.com/mikebird28/annt-python>`_  which read images annotated with annt.
you can load annotated images in a simple way and focus on the essential AI development.
Also, this library has a basic build-in preprocessing functions. So you can save time to write extra code.

Examples
============

Example 1. Load annotated images
:::::::::::::::::::::::::::::::::::

.. code-block::

   import annt

   # annotations is list of annotation data
   annotations = annt.load('./Dropbox/app/project_name')

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
      print(f'bottom : {box.bottom}')

      # If you change these coordination properties, all of them will recomputed.
      box.w = 300  # This operation will also change box.right property.


Example 2. Data augumentation
::::::::::::::::::::::::::::::

.. code-block:: python

   import annt
   import random

   # annotations is list of annotation data
   annotations = annt.load('./Dropbox/App/annt/test')
   sample_n = 10  # Number of samples from one image

   # Display ths information of each annotation file.
   augumented = []
   for raw_a in annotations:
      for i in range(sample_n):

         # Rotate image
         rot_deg = random.choice([0, 90, 180, 270, 360])
         a = raw_a.rotate(rot_deg)

         # Tilt image
         tilt_deg = random.randint(-8, 8)
         a = a.rotate(tilt_deg)

         # Flip image
         flip_x = random.randint(0, 1)
         flip_y = random.randint(0, 1)
         a = a.flip(flip_x, flip_y)
         augumented.append(a)

   # Show first augumented image.
   augumented[0].show()


Documents
============
.. automodule :: annt.main
   :members:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


from unittest import TestCase
from annt import load, load_annotation, show, Box

class TestAnnt(TestCase):

    def test_box(self):
        new_box = Box('tag', 100, 200, 10, 10, 50, 50)
        self.assertEqual(new_box.left, 10)
        self.assertEqual(new_box.top, 10)
        self.assertEqual(new_box.right, 40)
        self.assertEqual(new_box.bottom, 140)

        new_box.right = 10
        self.assertEqual(new_box.w, 80)
        new_box.bottom = 10
        self.assertEqual(new_box.h, 180)
        new_box.top = 10
        self.assertEqual(new_box.y, 10)
        self.assertEqual(new_box.bottom, 10)
        new_box.left = 30
        self.assertEqual(new_box.x, 30)
        self.assertEqual(new_box.right, 10)

    def test_load(self):
        path = "/Users/keisuke/Dropbox/アプリ/annt/test name/"
        annotations = load(path)
        for ant in annotations:
            ant.show()
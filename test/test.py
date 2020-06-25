
from unittest import TestCase
from annt import load, Box, hsv_to_rgb

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
        path = "/Users/keisuke/Dropbox/アプリ/annt/test/"
        annotations = load(path)
        for a in annotations:
            a.show()
            break

    def test_preprocess(self):
        path = "/Users/keisuke/Dropbox/アプリ/annt/test/"
        annotations = load(path)
        for a in annotations:
            a = a.rotate(5)
            a = a.resize(500, 500)
            a = a.flip(True, True)
            a.show()

class TestColor(TestCase):

    def test_hsv_to_rgb(self):
        colors = [
            ((255, 0, 0), (0, 1, 1)),
            ((255, 255, 255), (0, 0, 1)),
            ((85, 89, 153), (237, 0.44, 0.60)),
        ]
        for rgb, hsv in colors:
            self.assertTupleEqual(rgb, hsv_to_rgb(*hsv))

if __name__ == "__main__":
    unittest.main()
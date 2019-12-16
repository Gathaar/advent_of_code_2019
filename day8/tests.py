from .day8 import render_image
import unittest


class TestMySelfies(unittest.TestCase):
    def test_day8_0(self):
        raw_input = '123456789012'
        width = 3
        height = 2

        layers = render_image(raw_input, width, height)
        self.assertEqual(2, len(layers))        # Verify layer count
        self.assertEqual(2, len(layers[0]))     # Verify height
        self.assertEqual(['7', '8', '9'], layers[1][0])

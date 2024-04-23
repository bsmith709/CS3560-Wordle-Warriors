import unittest

class TestGetOffset(unittest.TestCase):
    def test_valid_input1(self):
        self.assertEqual(getOffset(0, 5), 10)  # Test with frame=0 and frames_per_letter=5

    def test_valid_input2(self):
        self.assertEqual(getOffset(5, 11), 30)  # Test with frame=5 and frames_per_letter=11

    def test_boundary_value(self):
        self.assertEqual(getOffset(0, 1), 30)  # Test with frame=0 and frames_per_letter=1

def getOffset(frame, frames_per_letter):
    letter_frame = frame % frames_per_letter
    y_offset = 0
    mid_frame = ((frames_per_letter - 1) / 2)
    px_per_frame = 30 / (mid_frame + 1)
    if letter_frame <= mid_frame:
        y_offset = (letter_frame + 1) * px_per_frame
    else:
        y_offset = (frames_per_letter - letter_frame) * px_per_frame
    return y_offset

if __name__ == '__main__':
    unittest.main()

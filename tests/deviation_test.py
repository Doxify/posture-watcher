import sys
sys.path.append('../src')

import unittest
from deviation import Deviation
from posture import PostureWatcher


class TestDeviationClass(unittest.TestCase):

    def setUp(self):
        self.deviation = Deviation()

    def test_class_exists(self):
        self.assertIsInstance(self.deviation, Deviation)

    def test_class_has_attributes(self):
        self.assertTrue(hasattr(self.deviation, '_threshold'))
        self.assertTrue(hasattr(self.deviation, '_max_buffer'))
        self.assertTrue(hasattr(self.deviation, '_current_buffer'))
        self.assertTrue(hasattr(self.deviation, '_current_deviation'))
        self.assertTrue(hasattr(self.deviation, '_last_updated'))
        self.assertTrue(hasattr(self.deviation, '_last_deviation_passed_threshold'))

    def test_class_has_correct_default_attributes(self):
        self.assertEqual(self.deviation._threshold, 30)
        self.assertEqual(self.deviation._max_buffer, 0)


class TestHasDeviatedMethod(unittest.TestCase):

    def setUp(self):
        self.pw_with_buffer = PostureWatcher(deviation_buffer=2)
        self.pw_wout_buffer = PostureWatcher(deviation_buffer=0)

    def test_has_deviated_with_buffer(self):
        for i in range(0, self.pw_with_buffer.deviation.max_buffer):
            self.pw_with_buffer.deviation.current_deviation = self.pw_with_buffer.deviation.deviation_threshold + 1
            self.assertFalse(self.pw_with_buffer.deviation.has_deviated())  # buffer NOT reached

        self.assertTrue(self.pw_with_buffer.deviation.has_deviated())  # buffer reached

    def test_has_deviated_without_buffer(self):
        self.pw_wout_buffer.deviation.current_deviation = self.pw_wout_buffer.deviation.deviation_threshold + 1
        self.assertTrue(self.pw_wout_buffer.deviation.has_deviated())  # no buffer, so always true

    def tearDown(self) -> None:
        self.pw_with_buffer.stop()
        self.pw_wout_buffer.stop()


if __name__ == '__main__':
    unittest.main()

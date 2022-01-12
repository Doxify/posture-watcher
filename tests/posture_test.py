import sys
sys.path.append('../src')
import unittest
from posture import PostureWatcher


class TestPostureWatcherClass(unittest.TestCase):

    def setUp(self):
        self.pw = PostureWatcher()

    def test_class_has_correct_attributes(self):
        self.assertTrue(hasattr(self.pw, 'detector'))
        self.assertTrue(hasattr(self.pw, 'deviation'))
        self.assertTrue(hasattr(self.pw, 'cap'))
        self.assertTrue(hasattr(self.pw, 'last_fps_calc_timestamp'))
        self.assertTrue(hasattr(self.pw, 'base_posture'))
        self.assertTrue(hasattr(self.pw, 'deviation_algorithm'))
        self.assertTrue(hasattr(self.pw, 'deviation_interval'))
        self.assertTrue(hasattr(self.pw, 'deviation_adjustment'))
        self.assertTrue(hasattr(self.pw, 'thread'))
        self.assertTrue(hasattr(self.pw, 'debug'))
        self.assertTrue(hasattr(self.pw, 'logger'))

    def test_class_has_default_parameters(self):
        self.assertEqual(self.pw.deviation_algorithm, 2)
        self.assertEqual(self.pw.deviation_interval, 5)
        self.assertEqual(self.pw.deviation_adjustment, 5)
        self.assertEqual(self.pw.deviation.deviation_threshold, 25)
        self.assertEqual(self.pw.deviation.max_buffer, 3)

    def tearDown(self):
        self.pw.stop()


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestPostureWatcherClass('test_default_parameters'))
    return test_suite


if __name__ == '__main__':
    unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())

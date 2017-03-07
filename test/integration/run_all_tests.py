import test_jsonfairy, test_session
import unittest

if __name__ == "__main__":
    # python 2.6 doesn't support automatic test discovery without additional packages.
    # options: nosetest, unittest2 (backport of 2.7 unittest functionality)
    suite = unittest.TestSuite()
    suite.addTest(test_session.SessionTest('test_session'))
    suite.addTest(test_jsonfairy.JsonFairyTest('test_pixel_histograms'))
    unittest.TextTestRunner(verbosity=2).run(suite)

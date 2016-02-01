#! /usr/bin/env python
import unittest

if __name__ == '__main__':
    suite = unittest.TestLoader()
    tests = suite.discover('.')

    testSuite = unittest.TestSuite(tests)
    text_runner = unittest.TextTestRunner().run(testSuite)

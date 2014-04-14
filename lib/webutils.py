#!/usr/bin/env python
import os

def GetParameter(input, name, default_value):
    if name in input:
        return input[name]
    else: return default_value

def GetProjectRoot():
    dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.realpath("%s/../" % dir)

if __name__ == "__main__":
    import unittest
    class WebUtilTest(unittest.TestCase):
        def test_GetProjectRoot(self):
            rootpath = GetProjectRoot()
            dir,tail = os.path.split(rootpath)
            self.assertEqual(tail, "vcity")

        def test_GetParameter(self):
            input = {"key":"value"}
            self.assertEqual(GetParameter(input, "key", "default"), "value")
            self.assertEqual(GetParameter(input, "key1", "default"), "default")

    unittest.main()

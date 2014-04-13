#!/usr/bin/env python

import logging
import os
import shutil
import sys
import webutils

def SetupLog(dir = "./logs/", project_name = None):
    if project_name is not None:
        project = project_name # TODO add project caculate
    else:
        project = "common"
    logging.basicConfig(filename="%s/%s.log" % (dir, project),
            level = logging.DEBUG, filemode="a")

if __name__ == "__main__":
    import unittest
    class LogsTest(unittest.TestCase):
        def setUp(self):
            self.logdir = "../test/tmplog/"
            try:
                os.mkdir(self.logdir)
            except:
                pass

        def tearDown(self):
            shutil.rmtree(self.logdir)

        def test_SetupLog(self):
            SetupLog(dir = self.logdir, project_name = "project")
            self.assertTrue(os.path.exists("%s/%s.log" % (self.logdir, "project")))
            logging.info("Hello")
            self.assertTrue(open("%s/%s.log" % (self.logdir, "project")).read().
                    find("Hello") > 0)

    unittest.main()

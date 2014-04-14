import glob
import os
import sys
import importlib

if len(os.path.dirname(__file__)) > 0:
    path = os.path.dirname(__file__)
else:
    path = os.getcwd()
sys.path.append("%s/../logic/clazz/" % path)

import MySQLdb

def CreateTable(rpath):
    mods = glob.glob("%s/../logic/clazz/*.py" % rpath)
    print mods, "%s/../logic/clazz/*.py" % rpath, rpath
    names = (mod.split('/')[-1].split(".")[0] for mod in mods)
    mod_objs = (importlib.import_module(name) for name in names)
    for m in mod_objs:
        print m.GetCreateTableSQL()
    
if __name__ == "__main__":
    CreateTable(path)

import glob
import os
import sys
import importlib

if len(os.path.dirname(__file__)) > 0:
    path = os.path.dirname(__file__)
else:
    path = os.getcwd()
sys.path.append("%s/../logic/clazz/" % path)
sys.path.append("%s/../lib/" % path)

import MySQLdb
import sconfig
import accessor

def ConnectDB(config):
    return accessor.ConnectionPool("MySQLdb").GetItemByConfig(config)

def CreateTables(rpath):
    mods = glob.glob("%s/../logic/clazz/*.py" % rpath)
    names = (mod.split('/')[-1].split(".")[0] for mod in mods)
    mod_objs = (importlib.import_module(name) for name in names)
    for config in sconfig.dbconfig:
        conn = ConnectDB(config)
        csr = conn.cursor()
        for m in mod_objs:
            sql = m.GetCreateTableSQL()
            csr.execute(sql)
        csr.close()
        conn.close()

if __name__ == "__main__":
    CreateTables(path)

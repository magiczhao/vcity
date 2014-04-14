import sconfig
import serrcode
import entity
import hashlib
import json
import MySQLdb
import nametype
import redis
import StringIO

class ConnectionPool:
    def __init__(self, item_type):
        self.item_type = item_type 

    def Init(self, config):
        self.pool = config

    def GetItem(self, hash_value):
        if self.pool is None:
            raise Exception("ConnectionPool not Inited")
        config_item = self.pool[hash_value % len(self.pool)]
        if self.item_type == "MySQLdb":
            return MySQLdb.connect(host = config_item["host"],
                port = int(config_item["port"]), user = config_item['user'],
                passwd = config_item['passwd'], db = config_item['db'])
        else:
            return redis.StrictRedis(host = config_item['host'],
                port = int(config_item['port']))

class Accessor:
    def __init__(self):
        self.__db__ = ConnectionPool("MySQLdb")
        self.__cache__ = ConnectionPool("redis")
        self.is_inited = False
    
    def IsInited(self):
        return is_inited

    # set series for mock object
    def SetDbConnectionPool(self, connection):
        self.__db__ = connection

    def SetCacheConnectionPool(self, connection):
        self.__cache__ = connection

    def Init(self):
        self.__db__.Init(sconfig.dbconfig)
        self.__cache__.Init(sconfig.cacheconfig)
        self.is_inited = True

    def Get(self, entityobj):
        if self.GetFromCache(entityobj):
            return
        self.GetFromPermanent(entityobj)
    
    def Hash(self, key):
        hash_value = hashlib.md5(key)
        return int(hash_value.hexdigest(), 16)

    def GetFromCache(self, entityobj):
        meta = nametype.NameType(entityobj)
        if not meta.IsUseCache():
            return False
        key = entityobj.Key()
        # caculate which bucket to use
        cache = self.__cache__.GetItem(self.Hash(key))
        ret = cache.hget("h_%s" % meta.Table(), key)
        if ret is not None:
            item = json.loads(ret)
            entityobj.Set(item)
            return True
        return False

    def ConstructSetSQL(self, table, fields, conditions):
        # construct insert or update sql
        buffer = StringIO.StringIO()
        buffer.write("insert into %s set " % table)
        params = list()
        seprator = ""
        for f in fields:
            if type(fields[f]) is int:
                buffer.write(" %s%s=%%d" % (seprator, f))
            elif type(fields[f]) is str:
                buffer.write(" %s%s=%%s" % (seprator, f))
            seprator = ","
            params.append(fields[f])
        buffer.write(" on duplicate key update ")
        seprator = ""
        for f in fields:
            if type(fields[f]) is int:
                buffer.write(" %s%s=%%d" % (seprator, f))
            elif type(fields[f]) is str:
                buffer.write(" %s%s=%%s" % (seprator, f))
            params.append(fields[f])
            seprator = "," 
        return buffer.getvalue(), params

    def ConstructGetSQL(self, table, fields, conditions):
        # construct select sql
        buffer = StringIO.StringIO()
        buffer.write("select ")
        seprator = ""
        for f in fields:
            buffer.write("%s%s" % (seprator, f))
            seprator = ","
        buffer.write(" from %s " % table)
        buffer.write("where")
        params = list()
        seprator = ""
        for f in conditions:
            value = conditions[f]
            params.append(value)
            if type(value) is int:
                buffer.write(" %s%s=%%d" % (seprator,f))
            elif type(value) is str:
                buffer.write(" %s%s=%%s" % (seprator, f))
            seprator = ","
        
        sql = buffer.getvalue()
        return sql, params

    def GetFromPermanent(self, entityobj):
        meta = nametype.NameType(entityobj)
        conditions = entityobj.GetConditionParams()
        fields = entityobj.GetFieldParams()
        sql, params = self.ConstructGetSQL(meta.Table(), fields, conditions)
        key = entityobj.Key()
        db = self.__db__.GetItem(self.Hash(key))
        cursor = db.cursor()
        cursor.execute(sql, params)
        desc = cursor.description
        if not cursor.with_rows:
            raise serrcode.VCityException("no data fetched")

        while True:
            record = cursor.fetchone()
            dct = dict()
            if record is not None:
                for (name, value) in zip(desc, record):
                    dct[name[0]] = value
                if not meta.IsCollection():
                    entityobj.Set(dct)
                    break
                else:
                    entityobj.Append(dct)
            else: break
        self.SaveToCache(entityobj)

    def Set(self, entityobj):
        meta = nametype.NameType(entityobj)
        if meta.IsCollection():
            for item in entityobj:
                self.Set(item)
        else:
            dbres = self.SaveToPermanent(entityobj)
            cacheres = self.SaveToCache(entityobj)
            return dbres, cacheres

    def SaveToPermanent(self, entityobj):
        meta = nametype.NameType(entityobj)
        conditions = entityobj.GetConditionParams()
        fields = entityobj.GetFieldParams()
        sql, params = self.ConstructSetSQL(meta.Table(), fields, conditions)
        key = entityobj.Key()
        db = self.__db__.GetItem(self.Hash(key))
        cursor = db.cursor()
        return cursor.execute(sql, params)

    def SaveToCache(self, entityobj):
        meta = nametype.NameType(entityobj)
        value = json.dumps(entityobj.Get())
        key = entityobj.Key()
        cache = self.__cache__.GetItem(self.Hash(key))
        ret = cache.hset("h_%s" % meta.Table(), key, value)
        return ret

class MockConnectionPool:
    def __init__(self, item_type):
        self.item_type = item_type

    def Init(self):
        return

    def GetItem(self, key):
        if self.item_type == "MySQLdb":
            return MockMySQLdb()
        else:
            return MockRedis()

class MockMySQLdb:
    def cursor(self):
        return MockMysqlCursor()

class MockMysqlCursor:
    def __init__(self):
        self.description = ('field1', 'field2')

    def execute(self, sql, params):
        return sql, params

    def fetchone(self):
        return (1, 2)
    
class MockRedis:
    def __init__(self):
        self.mp = dict()

    def hget(self, bucket, key):
        if key == 'cached':
            return json.dumps({'field1':1, 'field2':2})
        else:
            return None

    def hset(self, bucket, key, value):
        self.mp[key] = value
        return self

if __name__ == "__main__":
    import unittest
    class SEntity(entity.Entity):
        def __init__(self, key, accessor):
            entity.Entity.__init__(self, accessor)
            self.__keys__ = set(("key", "name", "field1"))
            self.__conditions__ = {"key":key}
            self.key = key

        def Key(self):
            return self.__conditions__["key"]

    class AccessorTest(unittest.TestCase):
        def setUp(self):
            self.accessor = Accessor()
            self.accessor.SetDbConnectionPool(MockConnectionPool("MySQLdb"))
            self.accessor.SetCacheConnectionPool(MockConnectionPool("redis"))

        def test_Save(self):
            sentity = SEntity("magic", self.accessor)
            sentity.name = "name"
            dbres, cacheres = self.accessor.Set(sentity)
            value = json.dumps(sentity.Get())
            self.assertEqual(cacheres.mp["magic"], value)

        def test_GetInCache(self):
            sentity = SEntity("cached", self.accessor)
            sentity.Load()
            self.assertEqual(sentity.field1, 1)
            try:
                value = sentity.field2
                self.assertTrue(False)
            except:
                pass

        def test_GetInPermanent(self):
            sentity = SEntity("not_cached", self.accessor)
            sentity.Load()

    unittest.main()

import nametype
import serrcode

class BaseEntity:
    def __init__(self):
        self.__dict__['__conditions__'] = dict()
        self.__dict__['__keys__'] = set()
        self.__dict__['__fields__'] = dict()
        self.__dict__['__accessor__'] = None
        self.__dict__['__items__'] = list()
    
    def DebugString(self):
        return str(self.__conditions__) + str(self.__fields__)

class Entity(BaseEntity):
    def __init__(self, accessor):
        BaseEntity.__init__(self)
        self.__dict__['__is_loaded__'] = False
        self.__dict__['__is_exist__'] = False
        self.__accessor__ = accessor

    def IsLoaded(self):
        return self.__is_loaded__

    def IsEmpty(self, string):
        return len(string.strip()) == 0

    def IsExist(self):
        if not self.__is_loaded__:
            raise serrcode.VCityException("exist is unknown not loaded")
        return self.__is_exist__

    def Load(self):
        if self.__accessor__:
            self.__is_loaded__ = True
            try:
                self.__accessor__.Get(self)
                self.__is_exist__ = True
            except VCityException:
                self.__is_exist__ = False
        else:
            raise serrcode.VCityException(
                "entity without accessor can't load or save")

    def Save(self):
        if self.__accessor__:
            self.__accessor__.Set(self)
        else:
            raise serrcode.VCityException(
                "entity without accessor can't load or save")

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__.get(key)
        if key in self.__keys__:
            return self.__fields__[key]
        raise Exception("'%s' not attribute" % key)

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
            return
        if key in self.__keys__:
            self.__fields__[key] = value
            return
        raise Exception("'%s' not attribute" % key)

    def Get(self):
        return self.__fields__

    def Set(self, value):
        self.__fields__ = value.copy()

    def GetConditionParams(self):
        return self.__conditions__

    def GetFieldParams(self):
        return self.__fields__

    def __getitem__(self, index):
        return self.__items__[index]
    # the functions must be overwrited in subclass
    def Key(self):
        raise Exception('Key not support in Entity')

    def Append(self, item):
        self.__items__.append(item)

if __name__ == "__main__":
    import unittest
    class IntEntity(Entity):
        def __init__(self):
            Entity.__init__(self, None)
            self.__conditions__ = {"id":"magic"}
            self.__keys__ = set(("field1", "field2"))

        def Key(self):
            return str(self.__class__.__name__)

    class EntityTest(unittest.TestCase):
        def setUp(self):
            self.entity = IntEntity()

        def test_EntityAttribute(self):
            self.entity.field1 = 1
            self.entity.field2 = 2
            self.assertEqual(self.entity.field1, 1)
            try:
                self.entity.failed = True
                self.assertTrue(False)
            except:
                pass

        def test_EntityParams(self):
            self.entity.field1 = 1
            conditions = self.entity.GetConditionParams()
            self.assertEqual(len(conditions), 1)
            self.assertTrue("id" in conditions)

            fields = self.entity.GetFieldParams()
            self.assertEqual(len(fields), 1)

        def test_SetGet(self):
            values = {"field1":1, "field2":2}
            self.entity.Set(values)
            self.assertEqual(self.entity.field1, 1)
            fields = self.entity.Get()
            for f in fields:
                self.assertEqual(fields[f], values[f])

        def test_CanNotLoadSave(self):
            try:
                self.entity.Load()
                self.assertTrue(False)
            except serrcode.VCityException:
                pass
            try:
                self.entity.Save()
                self.assertTrue(False)
            except serrcode.VCityException:
                pass

    unittest.main()


class NameType:
    def __init__(self, instance):
        self.target_type = instance.__class__
        parts = self.target_type.__name__.split("_")
        self.table = parts[0]
        self.parts = set(parts)

    def IsCollection(self):
        return "List" in self.parts

    def IsUseCache(self):
        return "Direct" not in self.parts

    def Table(self):
        return "Tbl_%s" % self.table

if __name__ == "__main__":
    import unittest
    class User:
        def IsCollection(self):
            return False

        def IsUseCache(self):
            return True
    
    class User_Direct:
        def IsCollection(self):
            return False

        def IsUseCache(self):
            return False

    class User_Direct_List:
        def IsCollection(self):
            return True

        def IsUseCache(self):
            return False

    class NameTypeTest(unittest.TestCase):
        def test_Normal(self):
            user = User()
            meta = NameType(user)
            self.assertEqual(meta.IsCollection(), user.IsCollection())
            self.assertEqual(meta.IsUseCache(), user.IsUseCache())
            self.assertEqual(meta.Table(), "User")

        def test_List(self):
            user = User_Direct_List()
            meta = NameType(user)
            self.assertEqual(meta.IsCollection(), user.IsCollection())
            self.assertEqual(meta.IsUseCache(), user.IsUseCache())
            self.assertEqual(meta.Table(), "User")

        def test_Cache(self):
            user = User_Direct()
            meta = NameType(user)
            self.assertEqual(meta.IsCollection(), user.IsCollection())
            self.assertEqual(meta.IsUseCache(), user.IsUseCache())
            self.assertEqual(meta.Table(), "User")

    unittest.main()

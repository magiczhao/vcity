import sys
import os
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/../../lib/" % dir)
import entity
import webutils

def CreateTable():
    sql = """
        create table if not exists Tbl_VUser (
            `id` char(36) not null,
            `nickname` char(32) not null,
            `register_date` datetime not null,
            `last_login` datetime not null,
            `birthday` date not null,
            `description` varchar(128) default null,
            `icon` char(16) default null,
            primary key (`id`)
        );
    )"""

class VUser(entity.Entity):
    def __init__(self, accessor, uid):
        entity.Entity.__init__(self, accessor)
        self.__conditions__["id"] = uid
        self.__keys__= set(("id", "nickname", "register_date", "last_login",
                "birthday", "description", "icon"))

    def GetSource(self):
        if self.id:
            parts = self.id.split("_")
            if len(parts) > 0:
                return parts[0]
        return "unknown"

if __name__ == "__main__":
    import unittest
    class MockAccessor:
        def Get(self, entity):
            entity.Set({
                "id" : "qq_test",
                "nickname" : "test_user"
                })

        def Set(self, entity):
            return

    class VUserTest(unittest.TestCase):
        def setUp(self):
            self.user = VUser(MockAccessor(), "qq_test")

        def test_Load(self):
            self.user.Load()
            self.assertEqual("qq_test", self.user.id)
            self.assertEqual("test_user", self.user.nickname)
            self.assertEqual("qq", self.user.GetSource())

    unittest.main()

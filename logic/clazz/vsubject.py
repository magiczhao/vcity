import os
import sys
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/../../lib/" % dir)
import entity
import webutils
import serrcode

def GetCreateTableSQL():
    sql = """create table if not exists `tbl_VSubject`(
        `id` char(36) not null,
        `name` varchar(256) not null,
        `category` char(16) not null,
        `icon` char(16) not null,
        `description` varchar(256) not null,
        `resource` varchar(16) not null,
        `favoriate` int not null,
        primary key (`id`)
    )"""

    return sql

class VSubject(entity.Entity):
    def __init__(self, accessor, sid):
        entity.Entity.__init__(self, accessor)
        self.__conditions__["id"] = sid
        self.__keys__ = set(("id", "name", "category", "icon",
            "description", "resource", "favoriate"))

    def Key(self):
        return self.__conditions__['id']

    def Validate(self):
        try:
            if self.IsEmpty(self.name) or \
                self.IsEmpty(self.category) or self.IsEmpty(resource) or \
                self.IsEmpty(self.id):
                raise serrcode.VCityException(
                    "subject id/category/resource/name is empty")
        except KeyError:
            raise serrcode.VCityException(
                    "subject id/category/resource/name is empty")

    def GetUrl(self, resource):
        return "http://%s" % resource

if __name__ == "__main__":
    import unittest

    class MockAccessor:
        def Get(self, entity):
            entity.Set({
                "id" : "sanguoyanyi", "name" : u"Three Country",
                "category" : "novel", "resource" : "surl.org/ResourceId",
                "icon":"surl.org/IconId"
                })

        def Set(self, entity):
            return

    class VSubjectTest(unittest.TestCase):
        def setUp(self):
            self.subject = VSubject(MockAccessor(), "sanguoyanyi")

        def test_Load(self):
            self.subject.Load()
            self.assertEqual(self.subject.category, "novel")
            self.assertEqual(self.subject.resource, "surl.org/ResourceId")

        def test_Validate(self):
            try:
                self.subject.Validate()
                self.assertFalse(True)
            except serrcode.VCityException:
                pass

        def test_GetUrl(self):
            url = self.subject.GetUrl("surl.org")
            self.assertEqual(url, "http://surl.org")

    unittest.main()

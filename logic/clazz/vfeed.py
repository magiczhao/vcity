import os
import sys
dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/../../lib/" % dir)
import entity
import webutils
import serrcode

def GetCreateTableSQL():
    sql = """create table if not exists `Tbl_VFeed`(
        `id` int not null,
        `object_id` char(36) not null,
        `category` char(16) not null,
        `content` varchar(256) not null,
        `favoriate` int not null,
        primary key (`id`),
        index idx_object(`object_id`, `category`)
    )"""
    return sql

class VFeed(entity.Entity):
    def __init__(self, accessor, id):
        entity.Entity.__init__(self, accessor)
        self.__conditions__["id"] = id
        self.__keys__ = set(('id', 'object_id', 'category', 'content',
            'favoriate'))

    def Validate(self):
        try:
            if self.IsEmpty(self.id) or self.IsEmpty(self.object_id) or \
                    self.IsEmpty(self.category):
                raise serrcode.VCityException(
                        "id or object_id or category is empty")
        except KeyError:
            raise serrcode.VCityException(
                    "id or object_id or category is empty")

    def Key(self):
        if "id" in self.__fields__:
            return self.__fields__['id']
        else:
            return self.__conditions__['id']

class VFeed_List(entity.Entity):
    def __init__(self, accessor):
        entiry.Entity.__init__(self, accessor, condition)
        self.__conditions__["object_id"] = condition["object_id"]
        self.__conditions__["category"] = condition["category"]

    def Key(self):
        return "%s_%s" % (self.__conditions__["object_id"],
                self.__conditions__["category"])

    def GetItem(self, index):
        item = self.__items__[index]
        feed = VFeed(self.__accessor__, item['id'])
        feed.Set(item)
        return feed

if __name__ == "__main__":
    pass

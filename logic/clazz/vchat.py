import os
import sys

def GetCreateTableSQL():
    sql = """
        create table if not exists `Tbl_VChat` (
            `id` char(36) not null,
            `nickname` char(32) not null,
            `register_date` datetime not null,
            `last_login` datetime not null,
            `birthday` date not null,
            `description` varchar(128) default null,
            `icon` char(16) default null,
            primary key (`id`)
        );
    """
    return sql

class VChat_List(entity.Entity):
    def __init__(self, accessor):
        entity.Entity().__init__(self, accessor)

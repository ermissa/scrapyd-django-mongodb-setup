# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo


class MongoDBPipeline(object):

    collection_name = 'records'

    def __init__(self, mongo_server, mongo_port, mongo_db_name):
        self.mongo_server = mongo_server
        self.mongo_port = mongo_port
        self.mongo_db_name = mongo_db_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get('MONGODB_SERVER'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_db_name=crawler.settings.get('MONGODB_DB')
        )

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(
            self.mongo_server,
            self.mongo_port
        )
        self.db = self.connection[self.mongo_db_name]

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

import os
from django.conf import settings
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from pymongo import MongoClient
import pymongo
from datetime import datetime


class MongoConnection(object):

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['test_db']

    def get_collection(self, name):
        self.collection = self.db[name]


class EntriesCollection(MongoConnection):

    def __init__(self):
        super(EntriesCollection, self).__init__()
        self.get_collection('raw_entries')

    def update_and_save(self, obj):
        if self.collection.find({'id': obj.id}).count():
            self.collection.update({"id": obj.id}, {'id': 123, 'name': 'test'})
        else:
            self.collection.insert_one({'id': 123, 'name': 'test'})

    def get_by_topic_name(self, topic_name):
        return self.collection.find({'topic': topic_name})

    def get_by_topic_url(self, url):
        return self.collection.find({'topic_url': url})

    def get_entry_counts_by_year(self, id):
        pipeline = [
            {
                '$match': {
                    'topic_id': id
                }
            },
            {
                '$project': {
                    'year': {
                        '$year': '$entry_create_date'
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'year': '$year',
                        'topic_id': id,
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    '_id': 1
                }
            }
        ]
        lresult = list(self.collection.aggregate(pipeline))
        return {
            'years': [year['_id']['year'] for year in lresult],
            'count': [year['count'] for year in lresult]
        }

    def get_topic_id(self, url):
        doc = self.collection.find_one({'topic_url': url})
        if doc != None:
            return doc['topic_id']
        else:
            return None

    def remove(self, obj):
        if self.collection.find({'id': obj.id}).count():
            self.collection.delete_one({"id": obj.id})


class TopicStatisticsCollection(MongoConnection):

    def __init__(self):
        super(TopicStatisticsCollection, self).__init__()
        self.get_collection('topic_statistics')

    def insert_statistics(self, stats):
        self.collection.insert_one(stats)
        return True

    def get_all_statistics(self):
        return self.collection.find()

    def get_all_statistics_distinct_by_topic_url(self):
        return self.collection.find().distinct('topic_url')

    def get_statistics_by_topic_url(self, url):
        return self.collection.find({'topic_url': url})

    def get_all_statistics_by_topic_id(self, id):
        return self.collection.find({'topic_id': id})

    def get_single_statistics_by_topic_id(self, id):
        doc = self.collection.find_one({'topic_id': id})
        if doc != None:
            return doc
        else:
            return None

import os
from pymongo import MongoClient

COLLECTION_NAME = 'chat'

class MongoRepository(object):
  def __init__(self):
    mongo_url = os.environ.get('MONGO_URL')
    self.db = MongoClient(mongo_url).chat

  def find_all(self, selector):
    return self.db.chat.find(selector)
 
  def find(self, selector):
    return self.db.chat.find_one(selector)
 
  def create(self, chat):
    return self.db.chat.insert_one(chat)

  def update(self, selector, chat):
    return self.db.chat.replace_one(selector, chat).modified_count
 
  def delete(self, selector):
    return self.db.chat.delete_one(selector).deleted_count

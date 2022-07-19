import pymongo

from scrapy import settings
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings

from itemadapter import ItemAdapter

settings = get_project_settings()

class DuplicatesPipeline:
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(settings["MONGODB_SERVER"])
        self.collection = self.connection.visualising_news.raw_articles

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        if self.collection.count_documents({"link": item["link"]}, limit=1):
            raise DropItem(f"Duplicate item found: {item!r}")
        return item


class MongoPipeline(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        self.connection = pymongo.MongoClient(settings["MONGODB_SERVER"])
        self.collection = self.connection.visualising_news.raw_articles

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert_one(dict(item))
            print("I added something!")

        return item

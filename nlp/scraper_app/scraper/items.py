from os import link
import scrapy

def remove_whitespace(value):
    return value.strip()


class BaseArticlesItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    text = scrapy.Field()
    short_desc = scrapy.Field()
    publisher = scrapy.Field()


class BBCArticlesItem(BaseArticlesItem):
    pass


class GuardianArticlesItem(BaseArticlesItem):
    pass


class AndreessenHorowitzArticlesItem(BaseArticlesItem):
    pass


class ZDNetArticlesItem(BaseArticlesItem):
    pass

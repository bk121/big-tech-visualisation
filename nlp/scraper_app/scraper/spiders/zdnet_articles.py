import scrapy
from scraper.items import ZDNetArticlesItem

class ZDNetSpider(scrapy.Spider):
    name = "zdnet_articles"

    start_urls = [
        "https://www.zdnet.com/topic/microsoft/rss.xml",
        "https://www.zdnet.com/topic/ibm/rss.xml",
        "https://www.zdnet.com/topic/google/rss.xml",
        "https://www.zdnet.com/topic/apple/rss.xml",
    ]

    def parse(self, response):
        for article in response.css("channel item"):
            article_link = article.css("link::text").get()
            if article_link is not None:
                yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        item = ZDNetArticlesItem()
        item["title"] = (response.xpath("//head/title/text()").get(),)
        item["date"] = (response.xpath("//time/@datetime").get(),)
        item["link"] = (
            response.xpath('//head/meta[@property="og:url"]/@content').get(),
        )
        item["text"] = (
            "\n".join(response.xpath('//div[@class="storyBody"]/p/text()').getall()),
        )
        item["short_desc"] = response.xpath(
            '//head/meta[@property="og:description"]/@content'
        ).get()
        item["publisher"] = "ZD Net"

        yield item

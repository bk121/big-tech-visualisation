import scrapy
from scraper.items import BBCArticlesItem


class BBCSpider(scrapy.Spider):
    name = "bbc_articles"

    start_urls = ["http://feeds.bbci.co.uk/news/technology/rss.xml"]

    def parse(self, response):
        for article in response.css("channel item"):
            article_link = article.css("guid::text").get()
            if article_link is not None:
                yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        item = BBCArticlesItem()
        item["title"] = (response.xpath("//head/title/text()").get(),)
        item["date"] = (response.xpath("//time/@datetime").get(),)
        item["link"] = (response.xpath('//head/link[@rel="canonical"]/@href').get(),)
        item["text"] = (
            "\n".join(
                response.xpath(
                    '//article//p[@class="ssrcss-1q0x1qg-Paragraph eq5iqo00"]/text()'
                ).getall()
            ),
        )
        item["short_desc"] = response.xpath(
            '//head/meta[@property="og:description"]/@content'
        ).get()
        item["publisher"] = "BBC"
        # hand the item back to the parse method
        yield item

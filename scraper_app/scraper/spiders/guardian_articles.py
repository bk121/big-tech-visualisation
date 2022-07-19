import scrapy
from scraper.items import GuardianArticlesItem


class GuardianSpider(scrapy.Spider):
    name = "guardian_articles"

    start_urls = ["https://www.theguardian.com/uk/technology/rss"]

    def parse(self, response):
        for article in response.css("channel item"):
            article_link = article.css("link::text").get()
            if article_link is not None:
                yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        item = GuardianArticlesItem()

        item["title"] = (response.xpath("//head/title/text()").get(),)
        item["date"] = (
            response.xpath(
                '//head/meta[@property="article:published_time"]/@content'
            ).get(),
        )
        item["link"] = (
            response.xpath('//head/meta[@property="og:url"]/@content').get(),
        )
        item["text"] = ("\n".join(response.css("body p::text").getall()[2:]),)
        item["short_desc"] = response.xpath(
            '//head/meta[@property="og:description"]/@content'
        ).get()
        item["publisher"] = "Guardian"
        yield item

import scrapy
from scraper.items import AndreessenHorowitzArticlesItem


class AndreessenHorowitzSpider(scrapy.Spider):
    name = "andreessen_horowitz_articles"

    start_urls = ["https://a16z.com/articles/feed/"]
    def parse(self, response):
        for article in response.css("item"):
            article_link = article.css("link::text").get()
            if article_link is not None:
                yield scrapy.Request(article_link, callback=self.parse_article)

    def parse_article(self, response):
        item = AndreessenHorowitzArticlesItem()

        item["title"] = (response.xpath("//head/title/text()").get(),)
        item["date"] = (
            response.xpath(
                '//head/meta[@property="article:published_time"]/@content'
            ).get(),
        )
        item["link"] = (
            response.xpath('//head/meta[@property="og:url"]/@content').get(),
        )
        item["text"] = ("\n".join(response.css("p::text").getall()[1:-3]),)
        item["short_desc"] = response.xpath(
            '//head/meta[@property="og:description"]/@content'
        ).get()
        item["publisher"] = "Andreessen Horowitz"

        yield item
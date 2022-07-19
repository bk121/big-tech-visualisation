import os
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "scraper.pipelines.MongoPipeline": 1,
    "scraper.pipelines.DuplicatesPipeline": 0,
}

MONGODB_SERVER = os.getenv("NEW_MONGODB_SERVER")
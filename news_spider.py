from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess
from sqlalchemy.exc import IntegrityError

from app import db
from models import News
from summarizer import summarize


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        categories = ["politics", "opinion", "money", "sports", "art-culture"]
        urls = [f"https://kathmandupost.com/{category}" for category in categories]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news_links = response.css("figure a::attr('href')").getall()[:10]
        yield from response.follow_all(news_links, callback=self.parse_news_data)

    def parse_news_data(self, response):
        news_url = response.url
        news_category = (
            response.css(".title--line__red a::attr('href')").get().split("/")[1]
        )
        news_headline = response.css("h1::text").get()
        paragraphs = response.css(".story-section p::text").getall()
        news_content = " ".join(para.strip() for para in paragraphs)
        news_published_date = (
            response.css(".updated-time::text").get().split(":")[1].strip()
        )

        news = News(
            url=news_url,
            category=news_category,
            headline=news_headline,
            summarized_body=summarize(news_content, 0.3),
            published_date=datetime.strptime(news_published_date, "%B %d, %Y"),
        )
        db.session.add(news)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def run_spider():
    process = CrawlerProcess()
    process.crawl(NewsSpider)
    process.start()

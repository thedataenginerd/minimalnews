import scrapy
from scrapy.crawler import CrawlerProcess


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
        try:
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
        except:
            return

        yield {
            "url": news_url,
            "category": news_category,
            "headline": news_headline,
            # "content": news_content,
            "published_date": news_published_date,
        }


process = CrawlerProcess(
    settings={
        "FEEDS": {
            "news.json": {
                "format": "json",
                "encoding": "utf8",
                "indent": 4,
            },
        },
    }
)

process.crawl(NewsSpider)
process.start()

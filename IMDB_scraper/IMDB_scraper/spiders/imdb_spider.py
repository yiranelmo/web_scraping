# to run
# scrapy crawl imdb_spider -o results.csv

import scrapy

class ImdbSpider(scrapy.Spider):

    name = 'imdb_spider'
    start_urls = ["https://www.imdb.com/title/tt0068646/"]

    def parse(self, response):

        url = response.url + "fullcredits"
        yield scrapy.Request(url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):

        name = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for list in name:
            url = "https://www.imdb.com" + list
            yield scrapy.Request(url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):

        actor_name = response.css("span.itemprop::text").get()
        tv_movies = response.css("div.filmo-row b a::text").getall()

        for i in tv_movies:
            yield {
                "actor": actor_name,
                "Movie_or_TV_name": i
            }

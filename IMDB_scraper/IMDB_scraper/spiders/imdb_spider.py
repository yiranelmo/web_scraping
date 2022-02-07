# to run
# scrapy crawl imdb_spider -o results.csv

import scrapy

class ImdbSpider(scrapy.Spider):

    name = 'imdb_spider'
    start_urls = ["https://www.imdb.com/title/tt0068646/"]

    def parse(self, response):
        """
        From the movie's main page,
        use this function to get to the Cast & Crew page.
        ------------------------
        This function does not return any data.
        """

        # url is the Cast & Crew page of the movie
        url = response.url + "fullcredits"
        # called `parse_full_credits` function use `callback` method
        yield scrapy.Request(url, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        From the Cast & Crew page,
        this function returns a'scrapy.Request' for each actor's page.
        ------------------------
        This function does not return any data.
        """

        # create a list of relative paths, one for each actor
        name = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        # yield the request to next function by each actor
        for list in name:
            url = "https://www.imdb.com" + list
            yield scrapy.Request(url, callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        """
        From the each actor's page,
        this function returns a dictionary for
        each of the movies or TV shows on which that actor has worked.
        ------------------------
        This function return a dictionary.
        """

        # get the actors' names
        actor_name = response.css("span.itemprop::text").get()

        # get the movies or TV shows which the actor has worked
        tv_movies = response.css("div.filmo-row b a::text").getall()

        # make the actors' names and tv_movies to a dictionary
        for i in tv_movies:
            yield {
                "actor": actor_name,
                "Movie_or_TV_name": i
            }
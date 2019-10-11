import scrapy


class ArxivSpider(scrapy.Spider):
    name = "arxiv"
    start_urls = [
        'https://arxiv.org/list/math/1901?500',
        'https://arxiv.org/list/cs/1901?500',
        'https://arxiv.org/list/physics/1901?500',
        'https://arxiv.org/list/stat/1901?500',
    ]

    def parse(self, response):
        for item in response.css('dd > div.meta'):
            authors = []
            list_authors = item.css("div.list-authors")
            for author in list_authors.css("a"):
                authors.append(author.get())
            with open('file.txt', 'w') as f:
                f.write((" ").join(authors)+'\n')

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
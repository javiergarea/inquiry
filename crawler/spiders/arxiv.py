import scrapy
import io
import PyPDF2


class ArxivSpider(scrapy.Spider):
    name = "arxiv"
    open('items.jl', 'w+').close()
    start_urls = [
        'https://arxiv.org/list/math/1901?500',
        'https://arxiv.org/list/cs/1901?500',
        'https://arxiv.org/list/physics/1901?500',
        'https://arxiv.org/list/stat/1901?500',
    ]

    def __init__(self):
        self.docID = 0

    def get_pdf_content_lines(response):
        reader = PyPDF2.PdfFileReader(io.BytesIO(response.body))
        for page in reader.pages:
            for line in page.extractText().splitlines():
                yield line

    def parse(self, response):
        list_links = response.css('span.list-identifier')

        for item in response.css('dd > div.meta'):
            list_authors = item.css("div.list-authors")
            list_authors = list_authors.css("a")
            list_titles = item.css('div.list-title')
            for x in range(len(list_titles)):
                yield {'docID': self.docID,
                       'title': list_titles[x].css('div.list-title::text').extract()[1][:-2],
                       'authors': list_authors.css("a::text").extract(),
                       'subjects': [item.css('span.primary-subject::text').get(), item.css('div.list-subjects::text').extract()[2][2:-2]],
                       'abstract': list_links[x].css('a::attr(href)').extract()[0],
                       'pdf': list_links[x].css('a::attr(href)').extract()[1]
                       }
                self.docID += 1

        #next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #  next_page = response.urljoin(next_page)
        #  yield scrapy.Request(next_page, callback=self.parse)

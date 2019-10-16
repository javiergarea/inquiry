import scrapy
import io
import PyPDF2
from twisted.internet import defer


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
        self.abstract = ''

    def parse(self, response):
        list_links = response.css('span.list-identifier')

        for item in response.css('dd > div.meta'):
            list_authors = item.css("div.list-authors")
            list_authors = list_authors.css("a")
            list_titles = item.css('div.list-title')
            for x in range(len(list_titles)):
                links = list_links[x].css('a::attr(href)').extract()
                pdf_url = "https://arxiv.org"+links[1]
                abstract_url = "https://arxiv.org"+links[0]
                yield {'docID': self.docID,
                    'title': list_titles[x].css('div.list-title::text').extract()[1][:-2],
                    'authors': list_authors.css("a::text").extract(),
                    'subject': item.css('span.primary-subject::text').get(),
                    'other-subjects': item.css('div.list-subjects::text').extract()[2][2:-2],
                    'abstract': abstract_url,
                    'pdf': pdf_url
                }
                self.docID+=1

    def parse_abstract(self, response):
        self.abstract = response.xpath('//*[@id="abs"]/blockquote/text()').extract()[0]


    def parse_pdf(self, url):
        request = scrapy.http.Response("https://arxiv.org"+url)
        reader = PyPDF2.PdfFileReader(io.BytesIO(response.body))
        for page in reader.pages:
            for line in page.extractText().splitlines():
                yield line


        #next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #  next_page = response.urljoin(next_page)
        #  yield scrapy.Request(next_page, callback=self.parse)

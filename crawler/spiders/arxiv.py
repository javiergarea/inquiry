import scrapy
import io
import PyPDF2
from twisted.internet import defer
from urllib.request import urlopen

ARXIV = 'https://arxiv.org'
CS_PATH = '/list/cs/1901?500'
MATH_PATH = '/list/math/1901?500'
PHYSICS_PATH = '/list/physics/1901?500'
STAT_PATH = '/list/stat/1901?500'


class ArxivSpider(scrapy.Spider):
    name = 'arxiv'
    start_urls = [
        ARXIV + CS_PATH,
        # ARXIV + MATH_PATH,
        # ARXIV + PHYSICS_PATH,
        # ARXIV + STAT_PATH
    ]

    def parse(self, response):
        yield scrapy.Request(url=response.url, callback=self.parse_basic)

    def parse_basic(self, response):
        docID = 0
        list_links = response.css('span.list-identifier')

        for item in response.css('dd > div.meta'):
            list_authors = item.css('div.list-authors')
            list_authors = list_authors.css('a')
            list_titles = item.css('div.list-title')
            for x in range(len(list_titles)):
                links = list_links[x].css('a::attr(href)').extract()
                meta_data = {
                    'links': links,
                    'pdf_url': ARXIV + links[1],
                    'abstract_url': ARXIV + links[0],
                    'docID': docID,
                    'title': list_titles[x].css('div.list-title::text').extract()[1][:-2],
                    'authors': list_authors.css('a::text').extract(),
                    'subject': item.css('span.primary-subject::text').get(),
                    'other_subjects': item.css('div.list-subjects::text').extract()[2][2:-2]
                }
                yield scrapy.Request(url=ARXIV + links[0], callback=self.parse_abstract, meta=meta_data)
                docID += 1

    def parse_abstract(self, response):
        response.meta.update({'abstract': response.xpath(
            '//*[@id="abs"]/blockquote/text()').extract()[0]})
        yield scrapy.Request(url=response.meta.get('pdf_url'), callback=self.parse_pdf, meta=response.meta)

    def parse_pdf(self, response):
        reader = PyPDF2.PdfFileReader(io.BytesIO(response.body))
        pdf = [
            line for page in reader.pages for line in page.extractText().splitlines()]
        response.meta.update({'pdf': pdf})
        yield response.meta

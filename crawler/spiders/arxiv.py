import io
import scrapy
import pdftotext
import datetime
import locale

ARXIV = 'https://arxiv.org'
CS_PATH = '/list/cs/1901?skip=0&show=500'
MATH_PATH = '/list/math/1901?skip=0&show=500'
PHYSICS_PATH = '/list/physics/1901?skip=0&show=500'
STAT_PATH = '/list/stat/1901?skip=0&show=500'


class ArxivSpider(scrapy.Spider):
    name = 'arxiv'
    start_urls = [
        ARXIV + CS_PATH,
        ARXIV + MATH_PATH,
        ARXIV + PHYSICS_PATH,
        ARXIV + STAT_PATH
    ]

    def __init__(self):
        self.doc_id = 0
        self.link = 0

    def parse(self, response):
        list_links = response.css('span.list-identifier')
        for item in response.css('dd > div.meta'):
            links = list_links[self.link].css('a::attr(href)').extract()
            meta_data = {
                'pdf_url': ARXIV + links[1],
                'abstract_url': ARXIV + links[0],
                'doc_id': self.doc_id,
                'title': item.css('div.list-title')[0]. \
                    css('div.list-title::text').extract()[1][:-1],
                'authors': item.css('div.list-authors').css('a').css('a::text').extract(),
                'subject': item.css('span.primary-subject::text').get(),
                'other_subjects': item.css('div.list-subjects::text').extract()[2][2:-2]
            }
            yield scrapy.Request(url=ARXIV + links[0], callback=self.parse_abstract,
                                 meta=meta_data)
            self.doc_id += 1
            self.link += 1

    def parse_abstract(self, response):
        response.meta.update({'abstract': response.xpath(
            '//*[@id="abs"]/blockquote/text()').extract()[0]})

        date_time_str = response.css('.dateline::text').get().replace('\n  ','')[21:-1]
        locale.setlocale(locale.LC_TIME, "en_US")
        if date_time_str:
            date_time = datetime.datetime.strptime(date_time_str, '%d %b %Y')
        else:
            date_time = None
        response.meta.update({'submit_date': str(date_time)})
        yield scrapy.Request(url=response.meta.get('pdf_url'), callback=self.parse_pdf,
                             meta=response.meta)

    def parse_pdf(self, response):
        reader = pdftotext.PDF(io.BytesIO(response.body))
        pdf = [page for page in reader]
        response.meta.update({'pdf': pdf})
        yield response.meta

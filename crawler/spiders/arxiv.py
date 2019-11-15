import io
import scrapy
import PyPDF2

ARXIV = 'https://arxiv.org'
CS_PATH = '/list/cs/1901?skip=0&show=100'
MATH_PATH = '/list/math/1901?skip=0&show=100'
PHYSICS_PATH = '/list/physics/1901?skip=0&show=100'
STAT_PATH = '/list/stat/1901?skip=0&show=100'


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
                    css('div.list-title::text').extract()[1][:-2],
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
        response.meta.update({'submit_date': response.css('.dateline::text').get().replace('\n  ','')[8:-1]})
        yield scrapy.Request(url=response.meta.get('pdf_url'), callback=self.parse_pdf,
                             meta=response.meta)

    def parse_pdf(self, response):
        reader = PyPDF2.PdfFileReader(io.BytesIO(response.body))
        pdf = [
            line for page in reader.pages for line in page.extractText().splitlines()]
        pdf = ''.join(pdf)
        response.meta.update({'pdf': pdf})
        yield response.meta

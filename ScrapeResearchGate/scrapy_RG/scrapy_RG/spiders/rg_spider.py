import scrapy


class QuotesSpider(scrapy.Spider):
    name = "researchGate"

    custom_settings = {
        'DOWNLOAD_DELAY': 3.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5.0,
        'AUTOTHROTTLE_MAX_DELAY': 60.0,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
    }


    def start_requests(self):
        urls = [
            'https://www.researchgate.net/institutions',
        ]
        for url in urls:
            print "URL: " + url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print "we are in parse"
        for institution in response.xpath('//a[@class="js-facility-url"]/@href').extract():
            print "INST: " + institution + "\n"
            request = scrapy.Request(response.urljoin(institution) + '/members', callback=self.parse_institution)
            request.meta['institution'] = institution
            yield request
        
        next_page = response.xpath('//div[@class="action-load-next"]/div[@class="loadmore-btn"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_institution(self, response):
        print "IN PARSE_INSTITUTION\n"
        print "instit: " + response.meta['institution'] + "\n"
        for member in response.xpath('//h5[@class="ga-top-coauthor-name"]/a/@href').extract():
            yield {
                'institution' : response.meta['institution'],
                'member' : member,
            }
 


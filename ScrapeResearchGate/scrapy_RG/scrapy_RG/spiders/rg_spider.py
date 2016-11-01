import scrapy

from elasticsearch import Elasticsearch

es = Elasticsearch()

from elasticsearch_dsl import DocType, String
from elasticsearch_dsl.connections import connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

class Researcher(DocType):
    name = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    institution = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    expertise = String(analyzer='snowball')
    location = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})

    class Meta:
        index = 'dataforgood'

Researcher.init()




class QuotesSpider(scrapy.Spider):
    name = "researchGate_temp"

    custom_settings = {
        'DOWNLOAD_DELAY': 25.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5.0,
        'AUTOTHROTTLE_MAX_DELAY': 60.0,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
    }


    def start_requests(self):
        urls_file = open('../urls_institutions.txt','r')
        urls = urls_file.readlines() 
        for url in urls:
            url = url.strip() + '/members'
            print "URL: " + url
            institution = url.split('/')[-2]
            print "INSTITUTION: " + institution
            request = scrapy.Request(url=url, callback=self.parse_institution_members)
            request.meta['institution'] = institution
            yield request

#### not used anymore
#    def parse(self, response):
#        print "we are in parse"
#        for institution in response.xpath('//a[@class="js-facility-url"]/@href').extract():
#            print "INST: " + institution + "\n"
#            request = scrapy.Request(response.urljoin(institution) + '/members', callback=self.parse_institution)
#            request.meta['institution'] = institution
#            yield request
#        
#        next_page = response.xpath('//div[@class="action-load-next"]/div[@class="loadmore-btn"]/a/@href').extract_first()
#        if next_page is not None:
#            next_page = response.urljoin(next_page)
#            yield scrapy.Request(next_page, callback=self.parse)


    def parse_institution_members(self, response):
        print "we are in PARSE_INSTITUTIONi_MEMBERS\n"
        print "instit: " + response.meta['institution'] + "\n"
        location = response.xpath('//div[@itemprop="location"]/text()').extract_first()
        for member_url in response.xpath('//h5[@class="ga-top-coauthor-name"]/a/@href').extract():
            request = scrapy.Request(response.urljoin(member_url), callback=self.parse_member)
            request.meta['institution'] = response.meta['institution']
            request.meta['member'] = response.xpath('//h5[@class="ga-top-coauthor-name"]/a[@href="' + member_url +'"]/text()').extract_first()
            request.meta['location'] = location
            yield request
        next_page = response.xpath('//a5[@class=" navi-next pager-link ajax-page-load"]/@href').extract_first()
        if next_page is not None:
            request = scrapy.Request(response.urljoin(next_page), callback=self.parse_institution_members)
            request.meta['institution'] = response.meta['institution']
            yield request
        
    def parse_member(self, response):
        print "we are in parse_member"
        expertise = response.xpath('//a[@class="keyword-list-token-text ga-keyword-pill"]/text()').extract()
        ###elastic search insertion
        researcher = Researcher(name=response.meta['member'], institution=response.meta['institution'], location=response.meta['location'], expertise=expertise)
	researcher.save()
        ########################
        yield {
            'institution' : response.meta['institution'],
            'member' : response.meta['member'],
            'location' : response.meta['location'],
            'expertise' : expertise,
        }





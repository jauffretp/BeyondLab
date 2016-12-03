import scrapy
import re

#from elasticsearch import Elasticsearch
#
#es = Elasticsearch()
#
#from elasticsearch_dsl import DocType, String
#from elasticsearch_dsl.connections import connections
#
## Define a default Elasticsearch client
#connections.create_connection(hosts=['localhost'])
#
#class Researcher(DocType):
#    name = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
#    institution = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
#    expertise = String(analyzer='snowball')
#    location = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
#
#    class Meta:
#        index = 'dataforgood'
#
#Researcher.init()




class QuotesSpider(scrapy.Spider):
    name = "rg_publications"

    custom_settings = {
        'DOWNLOAD_DELAY': 12.0,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5.0,
        'AUTOTHROTTLE_MAX_DELAY': 60.0,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
    }


    def start_requests(self):
        urls_file = open('../url_members.txt','r')
        urls = urls_file.readlines() 
        for url in urls:
            url = url.strip() + '/publications' 
            print "URL: " + url
            request = scrapy.Request(url=url, callback=self.download_publication_page)
            yield request


### at present parse_institution is not used, the crawler directly crawls the members page of the institution
    def parse_institution(self, response):
        institution = response.xpath('//span[@itemprop="name"]/text()').extract_first()
        location = response.xpath('//div[@itemprop="location"]/text()').extract_first()
        print "location: " + location
# add this if you want to restrict to French institutions only
#        match = re.match(r'^(.*), *France\s*$', location)
#        if match :
        request = scrapy.Request(url=response.urljoin('/members'), callback=self.parse_institution_members)
        request.meta['institution'] = institution
        request.meta['location'] = location
        print "url to parse: " + response.urljoin('/members')
        yield request
##############################################

    def parse_institution_members(self, response):
        institution = response.xpath('//span[@itemprop="name"]/text()').extract_first().encode('utf-8')
        institution_url = re.sub(r'\/members\/*\d*$','',response.url)
        location = response.xpath('//div[@itemprop="location"]/text()').extract_first()
        print "parse institution members"
        print "instit: " + institution
        print "location: " + location
        match = re.match(r'^(.*), *France\s*$', location) # add this if you want to restrict to French institutions only
        if match :
          print 'French institution, appending to ../url_french_institutions.txt'
          with open("../url_french_institutions.txt","a") as myfile:
              myfile.write(institution_url + " : " + institution + "\n")
          for member_url in response.xpath('//h5[@class="ga-top-coauthor-name"]/a/@href').extract():
              complete_url = 'https://www.researchgate.net/' + member_url
              request = scrapy.Request(complete_url, callback=self.parse_member)
              request.meta['institution'] = institution
              request.meta['institution_url'] = institution_url
              request.meta['member'] = response.xpath('//h5[@class="ga-top-coauthor-name"]/a[@href="' + member_url +'"]/text()').extract_first()
              request.meta['location'] = location
              yield request
          next_page = response.xpath('//a5[@class=" navi-next pager-link ajax-page-load"]/@href').extract_first()
          if next_page is not None:
              request = scrapy.Request(response.urljoin(next_page), callback=self.parse_institution_members)
              yield request
        
    def parse_member(self, response):
        print "we are in parse_member"
        with open('www.researchgate.net/profile/' + response.url.split('/')[-1], "w") as myfile:
            myfile.write(response.body)
        expertise = response.xpath('//a[@class="keyword-list-token-text ga-keyword-pill"]/text()').extract()
        yield {
            'institution' : response.meta['institution'],
            'institution_url' : response.meta['institution_url'],
            'member' : response.meta['member'],
            'member_url' : response.url,
            'location' : response.meta['location'],
            'expertise' : expertise,
        }


    def download_publication_page(self, response):
        print "we are in download_publication_page"
        with open('www.researchgate.net/profile/' + response.url.split('/')[-2] + '/publications' , "w") as myfile:
            myfile.write(response.body)


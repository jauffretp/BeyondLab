# -*- coding: utf-8 -*-
import scrapy


class CrawlLocalSpider(scrapy.Spider):
    name = "crawl_local"
    allowed_domains = ["localhost"]
    #start_urls = (
    #    'http://www.localhost/',
    #)


    def start_requests(self):
        urls_file = open('/Users/vitomandorino/Documents/dataForGood/BeyondLab/ScrapeResearchGate/scrapy_RG/list_publi','r')
        urls = urls_file.readlines()
        for url in urls:
            url = url.strip()
            print "URL: " + url
            request = scrapy.Request(url=url, callback=self.parse_publications)
            yield request


    def parse_publications(self, response):
	print "we are in parse_publications"
        publis = response.xpath('//span[@class="publication-title js-publication-title"]/text()').extract()
	member_url = 'https://www.researchgate.net/' + response.xpath('//a[@class="ga-profile-header-name"]/@href').extract_first()
	member_name = response.xpath('//a[@class="ga-profile-header-name"]/text()').extract_first()
        yield {
	    'member' : member_name,
            'member_url' : member_url,
            'publications' : publis,
        }

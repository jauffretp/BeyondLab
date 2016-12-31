# -*- coding: utf-8 -*-
import scrapy


class NesetwebSpiderSpider(scrapy.Spider):
    name = "nesetweb_spider"
    allowed_domains = ["nesetweb.eu"]
    start_urls = ['http://nesetweb.eu/fr/database-of-researchers/?list=1']

    def parse(self, response):
        for url_membre in response.xpath('//a[@class="name-cell"]/@href').extract():  # response.xpath('//*[@class="name-cell"]//text()').extract()
            request = scrapy.Request(response.urljoin(url_membre), callback=self.parse_membre)
            request.meta['member_url_provisoire'] = url_membre
            yield request


    def parse_membre(self, response):
         member = ' '.join(response.xpath('//div[@class="single-members-content-div"]//h1/text()').extract_first().split())
         expertise = [ ' '.join(s.split()) for s in response.xpath('//h2[normalize-space(text())="Domaines d\'expertise"]/following::ul[1]//li//text()').extract()]
         location = ' '.join([' '.join(s.split()) for s in response.xpath('//div[@class="localization"]/text()').extract()])
         member_url = response.xpath('//div[@class="web"]/a/@href').extract_first()
         if bool(not member_url or member_url.isspace()):
             member_url = response.meta['member_url_provisoire'] 
         institution = response.xpath('normalize-space(//div[@class="affiliation-single"]/p/text())').extract()
#         institution_url = 
         yield {
             'member' : member,
             'expertise' : expertise,
             'location' : location,
             'member_url' : member_url,
             'institution' : institution,
         }

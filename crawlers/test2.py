import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from craigslist_sample.items import CraigslistSampleItem
import os.path

class MySpider(CrawlSpider):
    name = "craigs"
    allowed_domains = ["www.ratemyprofessors.com"]
    start_urls = ["http://www.ratemyprofessors.com/search.jsp?queryBy=teacherName&queryoption=HEADER&query=tamu&facetSearch=true"]

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="nextLink"]',)), callback="parsee", follow= True),
    )

    def parsee(self, response):
        profiles = response.xpath('//li[@class="listing PROFESSOR"]/a/@href').extract()
        print "the list of it ",len(profiles)
		  # for each of those links
        for profile in profiles:
            # define item
            professor = CraigslistSampleItem();

            # add profile to professor
            professor["profile"] = profile

            # pass each page to the parse_profile() method
            request = scrapy.Request("http://www.ratemyprofessors.com"+profile,
                 callback=self.parser_profile)
            request.meta["professor"] = professor

            # add professor to array of professors
            yield request
    def write_in_file(filename,content):
		     new_file=open(filename,'a')
		     new_file.write(content)
		     new_file.close()
    def parser_profile(self, response):
        professor = response.meta["professor"]

        if response.xpath('//*[@class="pfname"]'):
            # scrape each item from the link that was passed as an argument and add to current professor
            professor["firstMiddleName"] = response.xpath('//h1[@class="profname"]/span[@class="pfname"][1]/text()').extract() 
            professor["department"]=response.xpath('//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[2]/text()').extract()
        if response.xpath('//*[@class="plname"]'):
            professor["lastName"] = response.xpath('//h1[@class="profname"]/span[@class="plname"]/text()').extract()
        if response.xpath('//*[@class="comments"]'):
			  professor["comments"]=response.xpath('//*[@class="comments"]/p/text()').extract()
        if response.xpath('//*[@class="table-toggle rating-count active"]'):
            professor["numOfRatings"] = response.xpath('//div[@class="table-toggle rating-count active"]/text()').extract()

        if response.xpath('//*[@class="grade"]'):
            professor["overallQuality"] = response.xpath('//div[@class="breakdown-wrapper"]/div[@class="breakdown-header"][1]/div[@class="grade"]/text()').extract()
            professor["Helpfulness"]=response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/text()').extract()
            professor["Clarity"]=response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/text()').extract()
            professor['Easiness']=response.xpath('//*[@id="mainContent"]/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]/text()').extract()
        if response.xpath('//*[@class="grade"]'):
            professor["averageGrade"] = response.xpath('//div[@class="breakdown-wrapper"]/div[@class="breakdown-header"][2]/div[@class="grade"]/text()').extract()
        
        
        
        

        return professor
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

        
        
        
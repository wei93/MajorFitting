# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CraigslistSampleItem(Item):
    numOfPages = Field() # number of pages of professors (usually 476)
	
    firstMiddleName = Field() # first (and middle) name
    department=Field()

    lastName = Field() # last name
    numOfRatings = Field() # number of ratings
    overallQuality = Field() # numerical rating
    averageGrade = Field() # letter grade
    comments=Field()
    Helpfulness=Field()
    Clarity=Field()
    Easiness=Field()


    profile = Field() # url of professor profile

    pass
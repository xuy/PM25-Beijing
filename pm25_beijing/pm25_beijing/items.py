# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Pm25BeijingItem(Item):
    hour = Field()
    saturation = Field()
    timestamp = Field()
    pass

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class HotelItem(scrapy.Item):
    # define the fields for your item here like:
    city = Field()
    name = Field()
    url =  Field()
    latitude = Field()
    longitude = Field()
    desc = Field()
    rating_stars = Field()
    score = Field()
    #reviews = Field()

    

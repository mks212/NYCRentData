# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentItem(scrapy.Item):
    # define the fields for your item here like:
    page = scrapy.Field()
    address = scrapy.Field()
    neighborhood = scrapy.Field()
    rent = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    broker = scrapy.Field()
    amenities = scrapy.Field()
   
    

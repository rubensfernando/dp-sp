# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class crimeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ano = scrapy.Field()
    mes = scrapy.Field()
    natureza = scrapy.Field()
    dp = scrapy.Field()
    valor = scrapy.Field()
    pass

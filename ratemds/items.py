# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RatemdsItem(scrapy.Item):
	doc_name = scrapy.Field()
	specialty = scrapy.Field()
	rating = scrapy.Field()
	num_reviews = scrapy.Field()
	


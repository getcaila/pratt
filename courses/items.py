# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PrattCourse(scrapy.Item):
	site = scrapy.Field()
	institution = scrapy.Field()
	school = scrapy.Field()
	course_name = scrapy.Field()
	course_id = scrapy.Field()
	course_description = scrapy.Field()
	course_section = scrapy.Field()
	course_section_credit = scrapy.Field()
	course_section_start = scrapy.Field()
	course_section_end = scrapy.Field()

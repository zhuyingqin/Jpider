# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from web.models import ExampleDotCom
class BotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ExampleDotComItem(DjangoItem):
    django_model = ExampleDotCom
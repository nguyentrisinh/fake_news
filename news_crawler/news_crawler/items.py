# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# from scrapy.contrib.djangoitem import DjangoItem
from scrapy_djangoitem import DjangoItem
from scrapy.item import Field

from crawler_engine.models import StartupModel


class StartupModelItem(DjangoItem):
    # fields for this item are automatically created from the django model
    django_model = StartupModel

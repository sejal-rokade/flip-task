# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
import re

def convertFloat(value):
    try:
        return float(value)
    except:
        return 0


def extractPrice(value):
    try:
        return re.sub(r'\D', '', value)
    except:
        return 0



class FlipkartItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst(),
    )
    rating = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip,convertFloat),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip,extractPrice,convertFloat),
        output_processor=TakeFirst(),
    )
    info = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=Join(","),
    )
    discount = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip,convertFloat),
        output_processor=TakeFirst(),
    )
    originalPrice = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip,extractPrice,convertFloat),
        output_processor=TakeFirst(),
    )

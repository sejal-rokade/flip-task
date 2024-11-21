import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.loader import ItemLoader
from flipkart.items import FlipkartItem

class LaptopSpider(scrapy.Spider):
    name = "laptop"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/search?q=laptops"]
 
 
    def start_requests(self):
        # GET request
        yield scrapy.Request(self.start_urls[0], meta={
            "playwright": True,
            "playwright_page_methods": [
                PageMethod('wait_for_load_state',"domcontentloaded"),
                PageMethod('wait_for_timeout',2000),
                PageMethod("screenshot", path="laptop.png", full_page=True),

            ]
            })

    def parse(self, response):
        laptopContainer = response.css('div._75nlfW')
        laptops = []
        for laptop in laptopContainer:
            lpItem = ItemLoader(item=FlipkartItem(), selector=laptop)
            lpItem.add_css('rating', 'div.XQDdHH::text')
            lpItem.add_css('info','ul.G4BRas  > li::text')
            lpItem.add_css('price','div.Nx9bqj._4b5DiR::text')
            lpItem.add_css("originalPrice", "div.yRaY8j.ZYYwLA::text")
            lpItem.add_css("discount", "div.UkUFwK::text")
            lpItem.add_css("title", "div.KzDlHZ::text")
            yield lpItem.load_item()
            
           


# -*- coding: utf-8 -*-
from urllib.parse import quote
import scrapy
from scrapy import Request
from scrapy_selenium_test.items import ScrapySeleniumTestItem


class TaobaoSpiderSpider(scrapy.Spider):
    name = 'taobao_spider'
    allowed_domains = ['www.taobao.com']
    # start_urls = ['https://s.taobao.com/search?q=']
    base_url = ['https://s.taobao.com/search?q=']

    def start_requests(self):
        for key in self.settings.get('KEYWORD'):
            for i in range(1,self.settings.get('MAX_SIZE')+1):
                url=self.base_url[0]+quote(key)
                yield Request(url,callback=self.parse,meta={'page':i},dont_filter=True)

    def parse(self, response):
        products=response.xpath("//div[@class='m-itemlist']//div[@class='items'][1]//div[contains(@class,'item')]")
        for product in products:
            item=ScrapySeleniumTestItem()
            item['price']=''.join([i.strip() for i in  product.xpath('.//div[contains(@class,"price")]//text()').extract()])
            item['title']=''.join([i.strip() for i in  product.xpath('.//div[contains(@class,"title")]//text()').extract()])
            item['shop']=''.join([i.strip() for i in  product.xpath('.//div[contains(@class,"shop")]//text()').extract()])
            item['image']=''.join([i.strip() for i in  product.xpath('.//div[@class="pic"]//img[contains(@class,"img")]/@data-src').extract()])
            item['deal']=product.xpath(".//div[contains(@class,'deal-cnt')]//text()").extract_first("0人付款")
            item['location']=product.xpath(".//div[contains(@class,'location')]//text()").extract_first("无")
            yield item
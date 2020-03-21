import scrapy
import pandas as pd
from ..items import AmazonItem


class amazonSpider(scrapy.Spider):
    name= "amazon"
    allowed_domains= ['amazon.com']
    data = pd.read_csv("asin.csv", encoding="ISO-8859-1")
    asin = data.asin
    start_urls= ["https://www.amazon.com/dp/"+i for i in asin]

    def parse(self, response):
        items= AmazonItem()
        try:
            asin= response.request.meta['redirect_urls'][0].strip('https://www.amazon.com/dp/')
        except:
            asin= 'NA'
        try:
            title= response.css('#productTitle::text').extract()[0].strip()
        except:
            title= 'NA'
        try:
            try:
                price= response.css('#priceblock_dealprice::text').extract()[0].strip()
            except:
                price= response.css('#priceblock_ourprice::text').extract()[0].strip()
        except:
            try:
                price= response.css('#comparison_price_row .comparison_baseitem_column::text').extract()[0].strip()
            except:
                price= "NA"
        try:
            image= response.css('#landingImage::attr(src)').extract()[0]
        except:
            image= 'NA'
        try:
            desc = response.css('#feature-bullets ul li span.a-list-item::text').extract()
            desc = [x.replace('\n', '').replace(' ', '').replace('\t', '') for x in desc]
            while "" in desc:
                desc.remove("")
            description= ('').join(desc)
        except:
            description= 'NA'
        items['ASIN']= asin
        items['TITLE']= title
        items['PRICE']= price
        items['IMAGE']= image
        items['DESCRIPTION']= description
        yield items

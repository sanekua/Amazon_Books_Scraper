# -*- coding: utf-8 -*-
import scrapy,re
from ..items import AmazonproductItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon'
    page_number = 2
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011&qid=1557076430&ref=sr_pg_1']

    def parse(self, response):
        items = AmazonproductItem()

        product_name = response.css('.a-color-base.a-text-normal').css('::text').extract()
        product_price = response.css('.a-spacing-top-small .a-price-whole').css('::text').extract()
        product_author = response.css('.a-color-secondary .a-size-base+ .a-size-base').css('::text').extract()
        product_image = response.css('.s-image::attr(src)').extract()

        def author_editing(corr):
            new_list = []
            for i in range(len(corr)):
                new_list.append(corr[i].strip())
            return new_list


        product_author = author_editing(product_author)

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = re.findall(r'\d+', str(product_price))
        items['product_image'] = product_image

        yield items

        next_page = 'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250227011&dc&page='\
                    +str(AmazonSpiderSpider.page_number)+'&fst=as%3Aoff&qid=1557071015&rnid=1250225011&ref=sr_pg_2'
        if AmazonSpiderSpider.page_number <= 5:
            print("This is page number : ", AmazonSpiderSpider.page_number)
            AmazonSpiderSpider.page_number +=1
            yield response.follow(next_page, callback=self.parse)

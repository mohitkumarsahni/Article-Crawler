# -*- coding: utf-8 -*-
#https://lifehacker.com/handle-for-gmail-brings-your-email-to-dos-and-calenda-1789488585#ZeroResult4
#https://lifehacker.com/top-10-gmail-tips-for-power-users-1787627908#ZeroResult4
#https://lifehacker.com/how-i-finally-organized-my-messy-inbox-with-sortd-1754956174#ZeroResult1
#http://www.ibtimes.com/gmail-search-options-how-find-things-easily-your-inbox-2622430#ZeroResult4

import time
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SearchSpider(CrawlSpider):
    name = 'search'
    start_urls = ('https://medium.com/search?q=email',
     'http://www.lifehacker.co.in/others/the-lifehacker-staffs-favorite-email-newsletters/articleshow/62060993.cms',
     'http://www.lifehacker.co.in/life/literally-email-like-a-boss/articleshow/61919370.cms',
     'http://www.ibtimes.co.in/',
     'http://www.ibtimes.com/gmail-search-options-how-find-things-easily-your-inbox-2622430#ZeroResult4',
     'https://www.themuse.com/advice/common-email-subject-lines-stop-using',
     'https://lifehacker.com/handle-for-gmail-brings-your-email-to-dos-and-calenda-1789488585#ZeroResult4',
     'https://lifehacker.com/top-10-gmail-tips-for-power-users-1787627908#ZeroResult4',
     'https://lifehacker.com/how-i-finally-organized-my-messy-inbox-with-sortd-1754956174#ZeroResult1'
    )

    rules = (Rule(LinkExtractor(deny_domains=['urbandictionary.com','cookpad.com','twitter.com','accounts.google.com','youtube.com','instagram.com','facebook.com','w3schools.com','en.wikipedia.org','kayak.co.in','kayak.com','drafts.csswg.org','pinterest.com','moneycontrol.com','shutterstock.com','amazon.com','ebay.com','flipkart.com','snapdeal.com','masslive.com','berkshiremuseum.org']),callback='parse_page',follow=True),)

    def parse_page(self, response):
        item = {}
        item['url']=response.url
        item['title']=response.css('title::text').extract_first()
        yield item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class SearchenginePipeline(object):
#     def process_item(self, item, spider):
#         return item

import scrapy
from scrapy.conf import settings
import pymongo
import json
import requests as rq

class MongoDBPipeline(object):
    
    token = 'a74ace548903d1a18e613fe843e86377'
    diffbotArticleUrl = 'https://api.diffbot.com/v3/article?token='+self.token+'&url='
    diffbotAnalyzUrl = 'https://api.diffbot.com/v3/analyze?token='+self.token+'&url='

    #collection_name = 'scrapy_items'
    itemTemp = {}

    coll_urlandtitle = 'urlandtitle'
    coll_diffbotResultsArticle = 'diffbotResultsArticle'

    keywords = ['email','emails','gmail','yahoo','inbox','hotmail','mail','manage','outlook','search','mobile email','features', 'email search features', 'inbox', 'overloaded inbox', 'gmail tips', 'messy inbox', 'sorting emails', 'organizing emails', 'schedule emails', 'snooze emails', 'gmail labs', 'gmail shortcuts','productivity']

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        #self.collection = db[settings['MONGODB_COLLECTION']]



    def articleRes_parse(self,response,i):
        diffArResTxt = json.loads(response)
        temp = {}
        i['isArticleChecked'] = 'true'
        i['articleFound'] = 'true'
        temp['author'] = diffArResTxt['objects'][0]['author']
        temp['authorUrl'] = diffArResTxt['objects'][0]['authorUrl']
        temp['pageUrl'] = diffArResTxt['objects'][0]['pageUrl']
        temp['text'] = diffArResTxt['objects'][0]['text']
        temp['articleTitle'] = diffArResTxt['objects'][0]['title']
        temp['estimatedDate'] = diffArResTxt['objects'][0]['estimatedDate']
        temp['siteName'] = diffArResTxt['objects'][0]['siteName']

        i['data'] = temp
        self.db[self.coll_diffbotResultsArticle].insert_one(dict(i))
        return i

    def analyzeRes_parse(self,response,i):
        diffAnResTxt = json.loads(response)
        if 'type' in diffAnResTxt:
            if(diffAnResTxt['type'] == 'article'):
                i['isAnalyzed'] = 'true'
                diffArRes = rq.get(self.diffbotArticleUrl+i['url'])
                self.articleRes_parse(diffArRes.text,i)
            else:
                i['isAnalyzed'] = 'true'
                i['type'] = diffAnResTxt['type']
                self.db[self.coll_urlandtitle].insert_one(dict(i))
                return i
        else:
            i['isAnalyzed'] = 'true'
            i['type'] = 'ERROR'
            self.db[self.coll_urlandtitle].insert_one(dict(i))
            return i

    def process_item(self, item, spider):
        score = 0
        for i in self.keywords:
            if(item['url'].find(i) != -1):
                score = score+1
        for i in self.keywords:
            if(item['title'].find(i) != -1):
                score = score+1

        if(score > 0):
            item['score'] = score
            diffAnRes = rq.get(self.diffbotAnalyzUrl+item['url'])
            self.analyzeRes_parse(diffAnRes.text,item)
        else:
            item['score'] = score
            self.db[self.coll_urlandtitle].insert_one(dict(item))
            return item

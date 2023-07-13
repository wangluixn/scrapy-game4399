# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_redis.spiders import RedisCrawlSpider
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import Redis
from datetime import datetime

#管道默认是不生效的，需要启动
class GamePipeline:
    #处理数据的专用方法
    def process_item(self, item, spider):
        item['spider_name'] = spider.name
        item['crawled'] = datetime.strftime(datetime.utcnow(), "%Y-%m-%d")
        print(item)
        return item

class RedisPipeline(object):
    conn = None
    def open_spider(self, spider):
        self.conn = Redis(host='127.0.0.1',port=6379)

    def process_item(self, item, spider):
        dic = dict(item)
        self.conn.lpush('game1',str(dic))
        return item

    def close_spider(self, spider):
        pass
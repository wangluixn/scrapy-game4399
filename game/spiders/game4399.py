import scrapy
from game.items import GameItem
#redis数据库启动的小问题
#redis-server.exe redis.windows.conf 
#启动Redis报错：Could not create server TCP listening socket 127.0.0.1:6379: bind: 处理方式
#redis-cli.exe
# shutdown
# exit
# redis-server.exe redis.windows.conf


class Game4399Spider(scrapy.Spider):
    name = "game4399"   #爬虫的名字，通过scrapy genspider game4399 4399.com 命令创建
    allowed_domains = ["4399.com"]   #允许的域名
    start_urls = ["http://www.4399.com/flash/"]   #起始页面

    def parse(self, response):     #该方法是默认用来解析网页的
        #print(response.text)
        #运行项目 scrapy crawl game4399
        # txt = response.xpath('//ul[@class="n-game cf"]/li/a/b/text()').extract()
        # print(txt)
        li_list = response.xpath('//ul[@class="n-game cf"]/li')
        item = GameItem()
        for li in li_list:
            item['name'] = li.xpath("./a/b/text()").extract_first()
            item['category'] =  li.xpath("./em/a/text()").extract_first()
            item['fx_date'] = li.xpath("./em/text()").extract_first()
            
            yield item  #不需要列表，不占内存，引擎来调用数据


        part_url = response.xpath('//*[@id="pagg"]/a[last()]/@href').extract_first()
        print(type(part_url))
        if 'htm' in str(part_url):
            part_url = response.urljoin(part_url)
            print(part_url)
            #构建请求对象
            yield scrapy.Request(
                url = part_url,
                callback = self.parse,
                )
        else:
            print('已经没有页面数据可以爬取！')


# 1。创建项目
# scrapy startproject 项目名称
# 2．进入项目
# cd 项目名称
# 3.创建爬虫
# scrapy https://www.itcast.cn/channel/teacher.shtml 名字 域名
# 4。可能需要修改start_urls,修改成你要抓取的那个页面
# 5．对数据进行解析,在spider里面的parse(response)方法中进行解析
# def parse(self, response):
#     response.text拿页面源代码response.xpath()
#     response. css()
#     解析数据的时候。需要注意。默认xpath()返回的是Selector对象.想要数据必须使用extract(）提取数据
#     extract_first()
#     yield dic 
# yield 返回数据-→把数据交给pipeline来进行持久化存储
# 6．在pipeline中完成数据的存储
# class 类名():
# def process_item(self, item,spider):
# item:数据
# spider:爬虫
# return item
#7．设置settings.py文件将pipeline进行生效设置
# ITEM_PIPELINES = {
# '管道的路径':优先级,优先级数越小,优先级越高
# }
# 8．运行爬虫
# scrapy crawl 爬虫的名字



            



# import scrapy
# from scrapy.crawler import CrawlerProcess
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging

# class MySpider1(scrapy.Spider):
#     # Your first spider definition
#     print 'teste2'

# class MySpider2(scrapy.Spider):
#     # Your second spider definition
#     print 'teste'

# configure_logging()
# runner = CrawlerRunner()

# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(MySpider1)
#     yield runner.crawl(MySpider2)
#     reactor.stop()

# crawl()
# reactor.run() # the script will block here until the last crawl call is finished

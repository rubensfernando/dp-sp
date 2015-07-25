import scrapy

class MySpider(scrapy.Spider):
	name = 'myspider'

	def start_requests(self):
		return [scrapy.FormRequest("http://www.example.com/login",
			formdata={'user': 'john', 'pass': 'secret'},
			callback=self.logged_in)]

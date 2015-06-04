import scrapy
import urllib
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import FormRequest

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Origin': 'http://www.ssp.sp.gov.br',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'http://www.ssp.sp.gov.br/novaestatistica/Pesquisa.aspx',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
}

class dpspSpider(scrapy.Spider):
    name = "dpsp"
    allowed_domains = ["ssp.sp.gov.br"]
    start_urls = [
        "http://www.ssp.sp.gov.br/novaestatistica/Pesquisa.aspx"
    ]

    def parse(self, response):
        # Performs authentication to get past the login form
        sel = Selector(response)

        return FormRequest.from_response(response,
        formdata={#'__EVENTTARGET':'ctl00$ContentPlaceHolder1$btnMensal',
        '__EVENTTARGET':sel.xpath("//input[@name='__VIEWSTATE']/@value").extract(),
        'ctl00$ContentPlaceHolder1$ddlAnos':2014,
        'ctl00$ContentPlaceHolder1$ddlRegioes':1,
        'ctl00$ContentPlaceHolder1$ddlMunicipios':565,
        'ctl00$ContentPlaceHolder1$ddlDelegacias':1469,
        '__VIEWSTATE': sel.xpath("//input[@name='__VIEWSTATE']/@value").extract(),'__EVENTVALIDATION': sel.xpath("//input[@name='__EVENTVALIDATION']/@value").extract()},
        callback=self.after_login)

    def after_login(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)
        pass

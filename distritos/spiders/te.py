import scrapy
from scrapy.selector import Selector
from scrapy.utils.python import *

class LoginSpider(scrapy.Spider):
    name = 'test'
    start_urls = ["http://www.ssp.sp.gov.br/novaestatistica/Pesquisa.aspx"]
    global years
    years = ['2012','2013','2014','2015']
    global y1
    global city
    global dp
    city = '565'
    dp = '1469'

    def parse(self, response):
        sel = Selector(response)
        requests = []
        for year in years:
            #y1 = year

            # print year
            #year = '2012'

            yield scrapy.FormRequest.from_response(
                response,
                formdata={'__EVENTTARGET':'ctl00$ContentPlaceHolder1$btnMensal',
                '__VIEWSTATE':sel.xpath("//input[@name='__VIEWSTATE']/@value").extract(),
                '__EVENTVALIDATION': sel.xpath("//input[@name='__EVENTVALIDATION']/@value").extract(),
                'ctl00$ContentPlaceHolder1$ddlAnos':year,
                'ctl00$ContentPlaceHolder1$ddlRegioes':'1',
                'ctl00$ContentPlaceHolder1$ddlMunicipios':city,
                'ctl00$ContentPlaceHolder1$ddlDelegacias':dp
                },
                dont_filter=True,
                callback=self.after_login
        )



    def after_login(self, response):
        # check login succeed before going on
        # if "authentication failed" in response.body:
        #     self.logger.error("Login failed")
        #     return
        # else:
        #     print response.headers
        #     filename = response.url.split("/")[-2]
        #     with open(filename, 'wb') as f:
        #         f.write(response.body)
        items = []
        sel = Selector(response)


        year = sel.xpath('//span[@id="ContentPlaceHolder1_repAnos_lbAno_0"]/text()').extract()[0]
        print response.xpath('//tbody/tr')
        print year

        for natureza in response.xpath('//tr[td]'):
            item = []
            for m, mes in enumerate(response.xpath('//th[@class="grid_headermes"]')):
                #print m
                #if m>0:
                subitem = {}
                subitem["ano"] = unicode_to_str(year)
                subitem["mes"] = unicode_to_str(mes.xpath('./text()').extract()[0])
                subitem["natureza"] = unicode_to_str(natureza.xpath('*[1]/text()').extract()[0])
                subitem["dp"] = dp
                subitem["valor"] = unicode_to_str(natureza.xpath('*['+str(m+2)+']/text()').extract()[0])
                item.append(subitem)

            items.append(item)

        #items.append(sel.xpath('//*[@class="grid_mes"]').extract())

        exportfile = open( "exported.json", "a")
        exportfile.write (str(items)+',')
        # content = response.xpath('//*[@id="ContentPlaceHolder1_repAnos_gridDados_0"]/tbody').extract()
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(str(response.body))

        # exportfile2 = open( "response.txt", "a")
        # exportfile2.write (str(natureza))

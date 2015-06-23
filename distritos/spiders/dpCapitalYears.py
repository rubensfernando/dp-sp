# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.utils.python import *
import HTMLParser
from django.utils.encoding import smart_str, smart_unicode
from distritos.items import crimeItem
import lxml.etree
import lxml.html
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup

#years = ['2012','2013','2014','2015']
years = ['2012']
# dps = ["1410","1246","1143","1067","1015","983","957","934","915","1478","1275","1265","1262","1259","1257","1256","1255","1254","1253","1252","1154","1153","1152","1151","1150","1149","1148","1147","1146","1145","1078","1077","1076","1075","1074","1073","1072","1071","1070","1069","1027","1026","1025","1024","1023","1022","1021","1020","1019","1018","994","993","992","991","990","989","988","987","986","985","966","965","964","963","962","961","960","959","945","943","942","941","940","938","937","926","925","923","921","919","917","910","909","908","907","905","904","903","902","901","1270","1269","1268","1267","1251","1144","1068","1017","984","958","935","916","900","1476","773","772","771","764","11","4","5","6","7","8","9","10","758","1469","1411"]
dps = ["1411"]

class dpsCapital(scrapy.Spider):
    name = 'capitalYear'
    start_urls = ["http://www.ssp.sp.gov.br/novaestatistica/Pesquisa.aspx"]
    #dp = '1469'

    def __init__(self):
      self.idP = 0
      self.eTarget = ''
      self.dp = ''
      self.city = ''
      self.year = ''

    def parse(self, response):
        sel = Selector(response)

        self.city = '565'

        for dpg in dps:
          self.dp = dpg

          for year in years:
            self.year = year

            yield scrapy.FormRequest.from_response(
                  response,
                  formdata={'__EVENTTARGET':'ctl00$ContentPlaceHolder1$btnMensal',
                  '__VIEWSTATE':sel.xpath("//input[@name='__VIEWSTATE']/@value").extract(),
                  '__EVENTVALIDATION': sel.xpath("//input[@name='__EVENTVALIDATION']/@value").extract(),
                  'ctl00$ContentPlaceHolder1$ddlAnos':self.year,
                  'ctl00$ContentPlaceHolder1$ddlRegioes':'1',
                  'ctl00$ContentPlaceHolder1$ddlMunicipios':self.city,
                  'ctl00$ContentPlaceHolder1$ddlDelegacias':self.dp
                  },
                  dont_filter=True,
                  callback=self.get_data
              )
        pass

    def get_data(self, response):
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
            crime = []
            for m, mes in enumerate(response.xpath('//th[@class="grid_headermes"]')):
                nat = natureza.xpath('*[1]/text()')
                nat_text = nat.extract()[0]

                subitem = crimeItem()
                subitem["ano"] = unicode_to_str(self.year)
                subitem["mes"] = unicode_to_str(mes.xpath('./text()').extract()[0],'utf-8')
                # subitem["natureza"] = unicode_to_str(natureza.xpath('*[1]/text()').extract()[0],'utf-8')
                subitem["natureza"] = nat_text.encode('utf-8')
                subitem["dp"] = self.dp
                subitem["valor"] = unicode_to_str(natureza.xpath('*['+str(m+2)+']/text()').extract()[0]).replace('.','')
                #crime.append(subitem)
                yield subitem

            # yield crime
            #items.append(crime)

        # exportfile = open( "exports/exported-"+ city +'-'+ dp +".json", "a")
        # exportfile.write (str(items) + ', ')

        filename = response.url.split("/")[-2]
        with open("exports/"+filename+".html", 'wb') as f:
          f.write(str(response.body))

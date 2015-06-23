# -*- coding: utf-8 -*-

# Scrapy settings for distritos project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'distritos'

SPIDER_MODULES = ['distritos.spiders']
NEWSPIDER_MODULE = 'distritos.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'distritos (+http://www.folha.uol.com.br)'

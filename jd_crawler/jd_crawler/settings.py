# Scrapy settings for jd_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'jd_crawler'

SPIDER_MODULES = ['jd_crawler.spiders']
NEWSPIDER_MODULE = 'jd_crawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jd_crawler (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARES = { 
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
	'jd_crawler.user_agent_middleware.SwitchUserAgent': 400
	}

ITEM_PIPELINES = [
	'jd_crawler.pipelines.JdCrawlerPipeline'
]

####### db setting ##############
HOST = 'localhost'
PORT = 3306
USER = 'root'
PWD = ''
DB = 'jd_site'
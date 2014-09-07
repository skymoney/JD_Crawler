#-*- coding:utf-8 -*-

#before request, check wheather crawled

import re

from scrapy.exceptions import IgnoreRequest

class Check_Dumplicate_Url:
	def process_request(self, request, spider):
		#return request
		sku = re.search(r'\d+', str(request.url)).group()
		#use redis to store crawled sku and url
		#if crawled stop crawling
		#currently redis, maybe bloom filter later
		raise IgnoreRequest("Already visited")
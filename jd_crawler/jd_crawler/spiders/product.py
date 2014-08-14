#-*- coding:utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from jd_crawler.items import Jd_Product

import requests

import re

class JD_Product_Spider(BaseSpider):
	name = 'jd_product'

	allowed_domains = ['jd.com']

	start_urls = ['http://item.jd.com/1191635301.html',
		#'http://item.jd.com/987887.html', 
		#'http://item.jd.com/999878.html', 
		#'http://item.jd.com/875169.html', 
		#'http://item.jd.com/1021777412.html'
		]

	price_url = 'http://p.3.cn/prices/get?skuid=J_'
	
	def parse(self, response):
		hxs = HtmlXPathSelector(response)

		jd = Jd_Product()

		jd['sku'] = re.search(r'\d+', str(response.url)).group()

		jd['name'] = hxs.select("//div[@id='name']/h1/text()").extract()[0]

		jd['price'] = eval(requests.get(self.price_url + jd['sku']).content)[0]['p']
		jd['img'] = hxs.select("//div[@id='spec-n1']/img/@src").extract()[0]

		seller_detail_list = hxs.select("//ul[@class='detail-list']/li")
		jd['sell_detail'] = []
		for li in seller_detail_list:
			if li.select('./a'):
				jd['sell_detail'].append(li.select('./text()').extract()[0].encode('utf-8') +\
					li.select('./a/text()').extract()[0].encode('utf-8'))
			else:
				jd['sell_detail'].append(li.select('./text()').extract()[0].encode('utf-8'))

		#crawl product info
		product_detail_trs = hxs.select("//div[@id='product-detail-2']/table/tr")

		product_detail_info = {}
		current_tag = 'default'
		for single_tr in product_detail_trs:
			if single_tr.select('./th').extract():				
				product_detail_info[single_tr.select('./th/text()').extract()[0].encode('utf-8')] \
					= {}
				current_tag = single_tr.select('./th/text()').extract()[0].encode('utf-8')
			if single_tr.select('./td').extract():
				info = single_tr.select('./td/text()').extract()
				try:
					product_detail_info[current_tag][info[0].encode('utf-8')] = info[1].encode('utf-8')
				except:
					product_detail_info[current_tag][info[0].encode('utf-8')] = ''
		jd['product_detail'] = product_detail_info
		
		product_content_ele = hxs.select("//div[@id='product-detail-3']/duv/text()")

		if product_content_ele:
			jd['product_wrap'] = product_content_ele.extract()[0].encode('utf-8')
		else:
			jd['product_wrap'] = ''

		return jd
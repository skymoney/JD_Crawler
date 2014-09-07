#-*- coding:utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import scrapy.http.response as s_response

from bs4 import BeautifulSoup

from product import JD_Product_Spider

class Category(BaseSpider):
	name = 'jd_category'

	start_urls = [
		#'http://list.jd.com/list.html?cat=670%2C671%2C672',
		#'http://list.jd.com/list.html?cat=9987,653,655',
		'http://www.jd.com/allSort.aspx',
		]

	allowed_domains = ['jd.com']

	def parse(self, response):
		#crawl whole site
		hxs = response.selector
		all_ava_cates = hxs.xpath("//div[@id='allsort']//a/@href").re(r'list\.jd\.com/.*\.html')
		
		for cate in all_ava_cates[2:5]:
			yield Request('http://' + cate, callback=self.category_parse)

	def category_parse(self, response):
		'''
		parse category info
		'''
		if type(response) == s_response.html.HtmlResponse:
			hxs = HtmlXPathSelector(response)

			#get sku list
			p_list = hxs.xpath("//ul[@class='list-h']/li")
			sku_list = []
			if hxs.select("//ul[@class='list-h']/li"):
				sku_list = [p.xpath('./@sku').extract()[0] for p \
					in hxs.xpath("//ul[@class='list-h']/li")]
			if hxs.select("//div[@id='plist']/div"):
				sku_list = [p.xpath('./@sku').extract()[0] for p \
					in hxs.xpath("//div[@id='plist']/div")]
			for sku in sku_list:
				yield Request('/'.join(['http://item.jd.com', sku + '.html']), 
					callback=JD_Product_Spider().parse)
				
			next_page_link = hxs.xpath("//div[@class='pagin fr']/a[@class='next']/@href")
			if next_page_link:
				if next_page_link.extract()[0].startswith("?"):
					yield Request('http://list.jd.com/list.html' + next_page_link.extract()[0], 
						callback=self.category_parse)
				elif next_page_link.extract()[0].startswith("http"):
					yield Request(next_page_link.extract()[0], callback=self.category_parse)
				else:
					pass
		else:
			#maybe cache using bs4 to deal
			dom = BeautifulSoup(response.body)
			
			if dom.find('div', id='plist').find_all('li'):
				p_list = dom.find('div', id='plist').find_all('li')

			if dom.find('div', id='plist').find_all('div'):
				p_list = dom.find('div', id='plist').find_all('div')
			
			sku_list = [p.get('sku', '') for p in p_list]

			for sku in sku_list:
				yield Request('/'.join(['http://item.jd.com', sku + '.html']), 
					callback=JD_Product_Spider().parse)
			
			next_page_a = dom.find('div', 
				class_='pagin fr').find('a', class_='next')
			if next_page_a:
				next_page_link = next_page_a.get('href')
				if next_page_link.startswith("?"):
					yield Request('http://list.jd.com/list.html' + next_page_link.extract()[0], 
						callback=self.category_parse)
				elif next_page_link.startswith("http"):
					yield Request(next_page_link, callback=self.category_parse)
				else:
					pass
#-*- coding:utf-8 -*-
import re
from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from jd_crawler.items import Jd_Review

class JD_Review_Spider(BaseSpider):
	'''
	crawl JD review data
	'''
	name = 'jd_review'

	#review page http://club.jd.com/review/875169-0-1-0.html

	start_urls = [
	#'http://item.jd.com/875169.html', 
	'http://club.jd.com/review/875169-0-1-0.html',
	]

	allowed_domains = ['jd.com']

	def parse(self, response):
		hxs = response.selector
		#crawl customer reviews
		comments_list = hxs.xpath("//div[@id='comments-list']/div[@class='mc']")


		for comment_hxs in comments_list:
			review = Jd_Review()

			review['user_name'] = ''.join(comment_hxs.xpath(".//div[@class='u-name']//text()").extract()).strip().encode('utf-8')
			try:
				review['user_page'] = comment_hxs.xpath(".//div[@class='u-name']/a/@href").extract()[0].encode('utf-8')
			except:
				review['user_page'] = ''
			try:
				review['user_level'] = comment_hxs.xpath(".//span[@class='u-level']/span[1]/text()").extract()[0].encode('utf-8')
				review['user_address'] = comment_hxs.xpath(".//span[@class='u-level']/span[2]/text()").extract()[0].encode('utf-8')
			except:
				review['user_level'] = ''
				review['user_address'] = ''

			review['star'] = comment_hxs.xpath(".//div[@class='i-item']/div[@class='o-topic']/span[1]/@class").extract()[0][-1]
			review['comment_date'] = comment_hxs.xpath(".//span[@class='date-comment']/a/text()").extract()[0]

			review['tags'] = map(lambda x: x.encode('utf-8'), 
				comment_hxs.xpath(".//div[@class='comment-content']//span[@class='comm-tags']//text()").extract())
			
			#针对不同的格式，可能出现tag，content，pic 中的任意
			if len(comment_hxs.xpath(".//div[@class='comment-content']/dl")) == 1:
				#only content
				review['content'] = ''.join(comment_hxs.xpath(".//div[@class='comment-content']/dl[1]/dd/text()").extract()).encode('utf-8').strip()
			elif len(comment_hxs.xpath(".//div[@class='comment-content']/dl")) >= 2:
				#tags so second is content
				review['content'] = ''.join(comment_hxs.xpath(".//div[@class='comment-content']/dl[2]/dd/text()").extract()).encode('utf-8').strip()
			else:
				review['content'] = ''

			#这里如果有 版本信息 需要再考虑一下
			if len(comment_hxs.xpath(".//div[@class='comment-content']/div[@class='dl-extra']/dl")) == 1:
				review['buy_date'] = comment_hxs.xpath(".//div[@class='comment-content']/div[@class='dl-extra']/dl[1]/dd/text()").extract()[0].encode('utf-8')
			else:
				review['buy_date'] = comment_hxs.xpath(".//div[@class='comment-content']/div[@class='dl-extra']/dl[2]/dd/text()").extract()[0].encode('utf-8')
			review['useful'] = re.search(r'\d+', ''.join(comment_hxs.xpath(".//div[@class='useful']//text()").extract()).encode('utf-8').strip()).group()

			yield review

		#crawl next page
		
		if hxs.xpath("//div[@class='pagin fr']/a[@class='next']").extract():
			yield Request(hxs.xpath("//div[@class='pagin fr']/a[@class='next']/@href").extract()[0])
		
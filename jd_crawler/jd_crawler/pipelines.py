#-*- coding:utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import settings

from jd_crawler.items import Jd_Review, Jd_Product

class JdCrawlerPipeline(object):
    def __init__(self):
        pass       

    def open_spider(self, spider):
        self.mysql_con = MySQLdb.connect(host=settings.HOST, user=settings.USER, 
            passwd=settings.PWD, port = settings.PORT)
        self.mysql_con.select_db(settings.DB)
        self.mysql_con.set_character_set('UTF8')
        self.cur = self.mysql_con.cursor()
        

    def process_item(self, item, spider):
        '''
    	with open(item['sku'] + '.dat', 'wb') as item_file:
    		item_file.write(item['name'] + '\n')
    		item_file.write(item['price'] + '\n')
    		for d in item['sell_detail']:
    			item_file.write(d + '\n')
    		item_file.write('###################################\n')
    		for key in item['product_detail']:
    			item_file.write(key + '\n')
    			item_file.write('-------------------------------------\n')
    			for v in item['product_detail'][key]:
    				item_file.write(v + ': ' + item['product_detail'][key][v] + '\n')
        		item_file.write('+++++++++++++++++++++++++++++++++++++\n')

        	item_file.write('######################################\n')
        	item_file.write(item['product_wrap'] + '\n')
        #return item
        '''
        
        #write data to mysql
        if isinstance(item, Jd_Product):
            to_sql = "insert into product_basic(sku, name, img, price) " +\
                "values('%s', '%s', '%s', '%s')"%(item['sku'], item['name'].encode('utf-8'), \
                    item['img'].encode('utf-8'), item['price'])
            try:
                self.cur.execute(to_sql)
                self.mysql_con.commit()
            except:
                print 'sql error'

        if isinstance(item, Jd_Review):
            #print item['content']
            with open('review.dat', 'ab') as review_file:
                review_file.write('Name: ' + item['user_name'] + '\n')
                review_file.write('Page: ' + item['user_page'] + '\n')
                review_file.write('Level & Location: ' + item['user_level'] + ' @ ' + item['user_address'] + '\n')
                review_file.write('Star: ' + item['star'] + ' @ ' + item['comment_date'] + '\n')
                review_file.write('Tags: ' + ' '.join(item['tags']) + '\n')
                review_file.write('Content: ' + item['content'] + '\n')
                review_file.write('Buy Date: ' + item['buy_date'] + '\n')
                review_file.write('Useful: ' + item['useful'] + '\n')
                review_file.write('++++++++++++++++++++++++++++++++\n')

    def close_spider(self, spider):
        self.cur.close()
        self.mysql_con.close()
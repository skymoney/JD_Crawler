# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class JdCrawlerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class Jd_Product(Item):
	sku = Field()
	name = Field()
	img = Field()
	price = Field()

	sell_detail = Field()
	product_detail = Field()
	product_wrap = Field()

	service = Field()

	product_content = Field()

class Jd_Review(Item):
	sku = Field()

	user_name = Field()
	user_page = Field()
	user_level = Field()
	user_address = Field()

	star = Field()
	comment_date = Field()

	tags = Field()
	content = Field()
	buy_date = Field()

	useful = Field()
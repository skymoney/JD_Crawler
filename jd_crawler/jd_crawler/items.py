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

	review = Field()
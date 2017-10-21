from scrapy import Spider
from ratemds.items import RatemdsItem
import scrapy

class MDSpider(Spider):
	name = "ratings_spider"
	allowed_urls = ['https://www.ratemds.com/']
	start_urls = ['https://www.ratemds.com/best-doctors/ny/new-york/?page=' + str(i+1) for i in range(4493)]

	def parse(self, response):
		doc_list = response.xpath('//h2[@class="search-item-doctor-name"]/a/@href').extract()
		doc_links = ['https://www.ratemds.com' + str(doc) for doc in doc_list]
		rating_linksOne = [link + str('?page=') + str(1) for link in doc_links]
		rating_linksTwo = [link + str('?page=') + str(2) for link in doc_links]
		rating_linksThree = [link + str('?page=') + str(3) for link in doc_links]
		rating_linksFour = [link + str('?page=') + str(4) for link in doc_links]
		rating_linksFive = [link + str('?page=') + str(5) for link in doc_links]
		ratings_links = rating_linksOne + rating_linksTwo + rating_linksThree + rating_linksFour + rating_linksFive

		for link in ratings_links:
			yield scrapy.Request(link, callback=self.parse_reviews)

	def parse_reviews(self, response):
		doc_name = response.xpath('//div[@class="col-sm-6"]/h1/text()').extract_first()
		specialty = response.xpath('//div[@class="search-item-info"]/a/text()').extract_first()
		cat_ratings = response.xpath('//div[@class="col-xs-3 rating-number"]//text()[1]').extract()
		cat_ratings = "".join(cat_ratings).split()

		item = RatemdsItem()
		item['doc_name'] = doc_name
		item['specialty'] = specialty
		item['cat_ratings'] = cat_ratings
		yield item


from scrapy import Spider
from ratemds.items import RatemdsItem
import scrapy

class MDSpider(Spider):
	name = "md_spider"
	allowed_urls = ['https://www.ratemds.com/']
	start_urls = ['https://www.ratemds.com/best-doctors/ny/new-york/?page=' + str(i+1) for i in range(4493)]

	def parse(self, response):
		doc_list = response.xpath('//h2[@class="search-item-doctor-name"]/a/@href').extract()
		doc_links = ['https://www.ratemds.com' + str(doc) for doc in doc_list]

		for link in doc_links:
			yield scrapy.Request(link, callback=self.parse_docs, meta={'link':link})

	def parse_docs(self, response):
		doc_name = response.xpath('//div[@class="col-sm-6"]/h1/text()').extract_first()
		specialty = response.xpath('//div[@class="search-item-info"]/a/text()').extract_first()
		gender = response.xpath('//div[@class="col-sm-3 col-md-4 search-item-extra"]/div[1]//a/text()').extract_first()
		num_reviews = response.xpath('//div[@class="star-rating-count"]/span/text()').extract_first()
		
		num_pages = num_reviews.encode('utf-8')
		num_pages = (int(num_reviews)/10)
		num_pages = int(round(num_pages,0))
		
		link = response.meta['link']
		review_links = [link + '\?page=' + str(i+1) + '\#ratings' for i in range(num_pages)]

		for rev_link in review_links:
			yield scrapy.Request(rev_link, callback=self.parse_reviews)

	def parse_reviews(self, response):
		reviews = response.xpath('//div[@class="rating"]').extract()

		for review in reviews:
			cat_ratings = response.xpath('//div[@class="col-xs-3 rating-number"]//text()').extract()
			cat_ratings = "".join(cat_ratings).split()

		
		item = RatemdsItem()
		item['doc_name'] = doc_name
		item['specialty'] = specialty
		item['gender'] = gender
		item['num_reviews'] = num_reviews
		item['cat_ratings'] = cat_ratings

		yield item
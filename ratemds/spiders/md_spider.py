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
			yield scrapy.Request(link, callback=self.parse_insur, meta={'doc_links':doc_links})

	def parse_insur(self, response):
		link = response.meta['doc_links']
		doc_name = response.xpath('//div[@class="col-sm-6"]/h1/text()').extract_first()
		insurances = response.xpath('//div[@class="insurance-provider"]/strong/text()').extract()
		specialty = response.xpath('//div[@class="search-item-info"]/a/text()').extract_first()
		gender = response.xpath('//div[@class="col-sm-3 col-md-4 search-item-extra"]/div[1]//a/text()').extract_first()
		num_reviews = response.xpath('//div[@class="star-rating-count"]/span/text()').extract_first()
		languages = response.xpath('//ul[@class="credentials list-inline list-comma-seperated"]//text()').extract()
		borough = response.xpath('//a[@href="/best-doctors/ny/brooklyn/"]/span/text()').extract_first()

		item = RatemdsItem()
		item['doc_name'] = doc_name
		item['specialty'] = specialty
		item['gender'] = gender
		item['num_reviews'] = num_reviews
		item['insurances'] = insurances
		item['languages'] = languages
		item['borough'] = borough

		yield item


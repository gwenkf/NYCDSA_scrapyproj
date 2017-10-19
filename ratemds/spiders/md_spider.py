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
		
		insur_links = [lnk + str('#insurance') for lnk in links]

		for links in insur_links:
			yield scrapy.Request(links, callback=self.parse_insur, meta={'links':links})

	def parse_insur(self, response):
		link = response.meta['links']
		try:
			insurances = response.xpath('//div[@class="insurance-provider"]/strong/text()').extract()
		except AttributeError:
			insurances = 'n/a'


		credentials_links = [url + str('#credentials') for url in link]

		for lnk in credentials_links:
			yield scrapy.Request(lnk, callback=self.parse_credens, meta={'link': link})

	def parse_credens(self, response):
		links = response.meta['link']
		try:
			languages = response.xpath('//ul[@class="credentials list-inline list-comma-seperated"]//text()').extract()
		except AttributeError:
			languages = 'n/a'

		reviews_start = links

		for link in reviews_start:
			yield scrapy.Request(link, callback=self.parse_revs, meta={'links':links})

	def parse_revs(self, response):
		reviews = response.xpath('//div[@class="rating-feature rating"]').extract()

		for review in reviews:
			score = response.xpath('//span[@class="value"]/text()').extract()
			category = response.xpath('//div[@class="type"]/text()').extract()


			item = RatemdsItem()
			item['doc_name'] = doc_name
			item['specialty'] = specialty
			item['gender'] = gender
			item['num_reviews'] = num_reviews
			item['insurances'] = insurances
			item['languages'] = languages
			item['score'] = score
			item['category'] = category

			yield item


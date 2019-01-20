from scrapy import Spider
from rent.items import RentItem
from scrapy import Request
import re

class RentSpider(Spider):
	
	name = "rent_spider"
	allowed_urls = ['https://www.renthop.com']
	start_urls = ['https://www.renthop.com/search/nyc']

	def parse(self, response):

		pages = response.xpath('//span[@class="d-none d-md-inline-block"]')
		pages = pages[2].extract()
		tot_pages =  int(re.findall('\d+', pages)[3])

		result_urls = ['https://www.renthop.com/search/nyc?&page={}'.format(x) for \
		x in range(1,tot_pages+1)]

		for url in result_urls:
			yield Request(url=url, callback=self.parse_result_page)

	def parse_result_page(self, response):

		#keep track of current page in case of interruption
		curr_page = response.xpath('//span[@class="d-none d-md-inline-block"]')
		curr_page = curr_page[2].extract()
		curr_page = int(re.findall('\d+', curr_page)[2])

		#listing tag
		listings = response.xpath('//div[@class="search-info pr-3 pl-3 pr-md-0 pl-md-4"]')

		for listing in listings:     
			page = curr_page #in case of interruption

			#address within listing:
			address = listing.xpath('./div/a/text()').extract_first()

			try:
				address = address.replace(",", "").strip()
			except:
				address = address.strip()

			neighborhood = listing.xpath('./div/div[2]/text()').extract_first()
			neighborhood = neighborhood.replace(",", ";").strip()  #replace commas for CSV export
			
			rent = listing.xpath('./div/table/tr/td/text()').extract_first()
			rent = re.findall('\d+', rent)
			rent = int("".join(rent)) #rent starts as list because of comma in $3,500

			beds = listing.xpath('./div/table/tr/td[2]/span/text()').extract_first()
			#studios will not have int values, all others will
			try:
				beds = re.findall('\d+', beds)[0]
			except:
				pass

			baths = listing.xpath('./div/table/tr/td[3]/span/text()').extract_first() 
			baths = int(re.findall('\d+', baths)[0])

			broker = listing.xpath('./div/div/a/text()').extract_first()
			#broker field is empty sometimes, non-crucial data, so missing values are ok
			try:
				broker = broker.strip()
			except:
				pass
			
			amenities = listing.xpath('./div/div[1]/text()').extract()[-1]
			try:
				amenities = amenities.replace("·", ";").strip()
			except:
				amenities = amenities.strip()

			item = RentItem()
			item['page'] = page
			item['address'] = address
			item['neighborhood'] = neighborhood
			item['rent'] = rent
			item['beds'] = beds
			item['baths'] = baths
			item['broker'] = broker
			item['amenities'] = amenities
			yield item




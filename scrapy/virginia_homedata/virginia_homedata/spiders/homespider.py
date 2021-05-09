import scrapy

#creating spider 
class HomespiderSpider(scrapy.Spider):
	name = 'homespider'
	allowed_domains = ['homes.com']
	start_urls = ['https://homes.com/virginia-beach-va/homes-for-sale']

#base url to concantenate partial url extracted from hrefs    
	base_url = 'https://homes.com'


#defining parse to get all links to all houses
	def parse(self, response):
		global count
		global max_page_count
		all_houses = response.xpath('//article')

#to select houses one after the other on page from all houses
		
		for each_house in all_houses:

			post_title = each_house.xpath('.//span/div[2]/div[3]/text()').extract_first()
			price = each_house.xpath('.//span/div[2]/div[1]/span[1]/text()').extract_first()
			try:
				beds = each_house.xpath('.//span/div[2]/div[2]/text()').extract_first().split(" | ")[0].split(" ")[0]
			except:
				beds = "N/A"
			
			try:
				baths = each_house.xpath('.//span/div[2]/div[2]/text()').extract_first().split(" | ")[1].split(" ")[0]
			except:
				baths = "N/A"

			try:
				size = each_house.xpath('.//span/div[2]/div[2]/text()').extract_first().split(" | ")[2].split(" ")[0]
			except:
				size = "N/A"
			location = each_house.xpath('.//span/div[2]/a/div/text()').extract_first()
			sub_link = each_house.xpath('.//span/div[2]/a/@href').extract_first()
			link = self.base_url + sub_link
			
			
			yield{
				'Property Type': post_title,
				'Price': price,
				'Number of Beds': beds,
				'Number of Baths': baths,
				'Size in Sqft': size,
				'Address': location,
				'Link': link
			}


#Here we is when scrapper moves to the next page
			next_page_url = response.xpath('//div[contains(@class, "flex items-center")]/a[@data-testid = "SR-PaginationNext"]/@href').extract_first()
			next_page_url = self.base_url + next_page_url
			yield scrapy.Request(next_page_url, callback=self.parse)
			

		

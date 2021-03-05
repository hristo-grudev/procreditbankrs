import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import ProcreditbankrsItem
from itemloaders.processors import TakeFirst


class ProcreditbankrsSpider(scrapy.Spider):
	name = 'procreditbankrs'
	start_urls = ['https://www.procreditbank.rs/blog']

	def parse(self, response):
		post_links = response.xpath('//div[@class="content"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1//span/text()').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "text-align-justify", " " ))] | //p').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="title-date"]/span/text()').get()

		item = ItemLoader(item=ProcreditbankrsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

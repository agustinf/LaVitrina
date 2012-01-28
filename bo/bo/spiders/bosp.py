from scrapy.selector import HtmlXPathSelector
from scrapy.selector import XmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import XPathItemLoader
from scrapy.http import Request
from bo.items import BoItem

class BoSpider(CrawlSpider):
	name = "bo"
	allowed_domains = ["hostnordic.com"]
	start_urls = ["http://dcms-d193b.aar0.dk.hostnordic.com/sitemap.aspx?ID=81626"]
	rules = (
		Rule(SgmlLinkExtractor(allow='[a-zA-Z_/-]+\.aspx\?ID=[0-9]+$'), callback='parse_category'),
	)
	def parse_category(self, response):
    	# The main selector we're using to extract data from the page
		hxs = HtmlXPathSelector(response)
    	# The XPath to website links in the directory page
		xpath = '//div[@class="ImageContainer"]/a/@href'
    	#xpath = '//title'
    	# Get a list of (sub) selectors to each website node pointed by the XPath
		sub_selectors = hxs.select(xpath)
		items = []
		for link in sub_selectors:
	 		item = BoItem()
	 		item['url'] = link.extract()
	 		request = Request('http://dcms-d193b.aar0.dk.hostnordic.com'+item['url']+'&xmloutput=true', callback=self.parse_product)
	 		request.meta['item'] = item
	 		yield request
	 		#items.append(item)
	
	def parse_product(self,response):
		xxs = XmlXPathSelector(response)
		item = response.meta['item']
		item['image'] = xxs.select('//URL_largeImage/text()').extract()
		return item

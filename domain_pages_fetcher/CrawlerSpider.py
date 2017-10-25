from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import scrapy
from scrapy.spiders import CrawlSpider

class DomainSpider(CrawlSpider):
    name = "ynet"
    allowed_domains = ["www.ynet.co.il"]
    start_urls = ["http://www.ynet.co.il"]
    visited = set()
    parsed = set()

    def parse(self, response):
        for link in LxmlLinkExtractor(allow=[".*" + self.name + ".*"]).extract_links(response):
            if link not in self.visited:
                self.visited.add(link)
                yield scrapy.Request(link.url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        if response.url not in self.parsed:
            self.parsed.add(response.url)

        if self.allowed_domains[0] in response.url and "articles" in response.url:
            filename = "pages/" + response.url.split('/')[-1].replace(",", "_").replace("?", "_")
            with open(filename, 'wb') as f:
                f.write(response.body)

        for link in LxmlLinkExtractor(allow=[".*" + self.name + ".*"]).extract_links(response):
            if link not in self.visited:
                self.visited.add(link)
                yield scrapy.Request(link.url, callback=self.parse_dir_contents)


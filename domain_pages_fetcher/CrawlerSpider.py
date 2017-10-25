from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import scrapy
from scrapy.spiders import CrawlSpider
from random import shuffle

class DomainSpider(CrawlSpider):
    name = "ynet"
    allowed_domains = ["www.ynet.co.il"]
    start_urls = ["http://www.ynet.co.il"]
    visited = set()
    parsed = set()

    def parse(self, response):
        links = LxmlLinkExtractor(allow=[".*" + self.name + ".*"]).extract_links(response)
        shuffle(links)
        for link in links:
            if link.url not in self.visited:
                self.visited.add(link.url)
                yield scrapy.Request(link.url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        if response.url not in self.parsed:
            self.parsed.add(response.url)
        else:
            return

        if self.allowed_domains[0] in response.url and "articles" in response.url:
            filename = self.name + "/" + response.url.split('/')[-1].replace(",", "_").replace("?", "_")
            with open(filename, 'wb') as f:
                f.write(response.body)

        links = LxmlLinkExtractor(allow=[".*" + self.name + ".*"]).extract_links(response)
        shuffle(links)
        for link in links:
            if link.url not in self.visited:
                self.visited.add(link.url)
                yield scrapy.Request(link.url, callback=self.parse_dir_contents)


import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request


class BookingCrawlspiderSpider(CrawlSpider):
    name = 'booking-crawlspider'
    allowed_domains = ['www.booking.com']
    start_urls = ['https://www.booking.com/searchresults.fr.html?lang=fr/']

    le_next = LinkExtractor(allow=(), restrict_xpaths='//a[contains(@class,"paging-next")]')
    rules = (
        Rule(le_next,follow=True),
    )

    def __init__(self, cities_path = None, *args, **kwargs):
        #cities = ["Mont+Saint+Michel","Saint+Malo","Lille"]
        cities = ["Mont+Saint+Michel"]
        self.cities = cities
        self.start_urls = self._build_start_urls(cities)
        super(CrawlSpider, self).__init__(*args, **kwargs)


    def _build_start_url(self, city:str):
        return f'https://www.booking.com/searchresults.fr.html?lang=fr&ss={city}'

    def _build_start_urls(self, cities: list):
        return [self._build_start_url(city) for city in cities]

    def start_requests(self):
        #start_urls = ['https://www.booking.com/searchresults.fr.html?lang=fr&ss=Saint+Malo']

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        #print(f'URL = {self.start_urls}')
        print("requests starting...")
        for url in self.start_urls:
            print(f'url={url}')
            yield Request(url, headers=headers, dont_filter=True)


    def parse_item(self, response):
        divs = response.xpath('//div[contains(@class,"sr_item_new")]')
        names = divs[0].xpath('descendant::span[contains(@class,"sr-hotel__name")]/text()').extract()
        print(f'type div={divs[0]}')
        print(f'name={names}')

        print('***********************************************************************')

        for div in divs:
            data_coords = div.xpath('descendant::a[contains(@class,"bui-link")]/@data-coords').extract()[0]
            url_hotel = div.xpath('descendant::a[contains(@class,"bui-link")]/@href').extract()[0]
            yield{
                'name' : div.xpath('descendant::span[contains(@class,"sr-hotel__name")]/text()').extract()[0].strip(),
                'url' :  url_hotel.split('?')[0],
                'latitude' : data_coords.split(',')[0],
                'longitude': data_coords.split(',')[1],
                'desc' : div.xpath('descendant::div[contains(@class,"hotel_desc")]/text()').extract()[0].strip(),
                'etoiles' : "99",
                'note' : div.xpath('descendant::div[contains(@class,"bui-review-score__badge")]/text()').extract()[0].strip(),
                'reviews' : div.xpath('descendant::div[contains(@class,"bui-review-score__text")]/text()').extract()[0].strip(),
            }

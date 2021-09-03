import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
from scrapy.utils.log import configure_logging

logger = logging.getLogger(__name__)

class BookingSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='bookingspylog.txt',
        format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )

    name = 'bookingspy'
    allowed_domains = ['booking.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    #hotel_extractor = LinkExtractor(allow=(), restrict_xpaths=('//div[contains(@class,"sr_item_new")]',), callback='parse_item', follow=False)
    #rule_hotel_details = Rule(hotel_extractor, callback='parse_item')
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': 'True',
    }

    def __init__(self, cities_path = None, *args, **kwargs):
        #cities = ["Mont+Saint+Michel","Saint+Malo","Lille"]
        cities = ["Auterive"]
        super(BookingSpider, self).__init__(*args, **kwargs)
        self.cities = cities
        self.start_urls = self._build_start_urls(cities)

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
        for url in self.start_urls:
            print(f'------------starting with url={url}')
            yield Request(url, headers=headers, dont_filter=True)

    def parse(self, response):
        with open('./booking-page-{}.html', 'w') as file_obj:
            file_obj.write(response.text)
        #self.parse_booking_page(response)
    
    #def parse_booking_page(self, response):
        
        logging.info('***********************************************************************')
        print('***********************************************************************')
        divs = response.xpath('//div[contains(@class,"sr_item_new")]')
        print(f'hotels in page= {len(divs)}')
        names = divs[0].xpath('descendant::span[contains(@class,"sr-hotel__name")]/text()').extract()
        print(f'name={names}')

        print('***********************************************************************')

        for div in divs:
            data_coords = div.xpath('descendant::a[contains(@class,"bui-link")]/@data-coords').get()
            url_hotel = div.xpath('descendant::a[contains(@class,"bui-link")]/@href').get()

            yield{
                'name' : div.xpath('descendant::span[contains(@class,"sr-hotel__name")]/text()').get().strip(),
                'url' :  url_hotel.split('?')[0],
                'latitude' : data_coords.split(',')[0], #first element is latitude
                'longitude': data_coords.split(',')[1], # second element is longitude
                'desc' : self._strip(div.xpath('descendant::div[contains(@class,"hotel_desc")]/text()').get()),
                'etoiles' : div.xpath('descendant::span[contains(@class,"bui-rating--smaller")]/@aria-label').get(),
                'note' : self._strip(div.xpath('descendant::div[contains(@class,"bui-review-score__badge")]/text()').get()),
                'reviews' : div.xpath('descendant::div[contains(@class,"bui-review-score__text")]/text()').get(),
            }

            try:
                next_page = response.xpath('//a[contains(@class,"paging-next")]/@href').get()
                print(f'next page type = {type(next_page)}')
                yield response.follow(next_page, callback = self.parse)
                
            except (ValueError, KeyError) as noNextKeyError:
                #logging.info('There is no next page. The crawling process will terminate')
                print('There is no next page. The crawling process will terminate')

    def _strip(self, text):
        if text is not None:
            return text.strip()
        return ''

    def _get_etoiles(self, text_etoiles):
        #Stars are defined in a text like this "2 out of 5". We retrieve only the first character
        return self._strip(text_etoiles).split(' ')[0]

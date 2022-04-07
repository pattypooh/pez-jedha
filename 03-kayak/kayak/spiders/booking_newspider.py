from email import header
from matplotlib import offsetbox
import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
from scrapy.utils.log import configure_logging

logger = logging.getLogger(__name__)

class NewBookingSpider(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='bookingspylog.txt',
        format='[%(asctime)s: %(levelname)s: - %(funcName)20s() ]%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
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
    def __init__(self, city = 'Toulouse', *args, **kwargs):
        if city is not None:
            cities = [city]
#        cities = ["Mont Saint Michel"]
        super(NewBookingSpider, self).__init__(*args, **kwargs)
        self.cities = cities
        self.start_urls = self._build_start_urls(cities)

    def _build_start_url(self, city:str):
        return f'https://www.booking.com/searchresults.fr.html?lang=fr&ss={city}'

    def _build_start_urls(self, cities: list):
        return [self._build_start_url(city) for city in cities]

    def start_requests(self):
        logging.debug('1. Starting all url requests')
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        cb_kwargs = {} # This dict is used to pass more parameters to parse() method
        for i, url in enumerate(self.start_urls):
            print(f'*****Starting with url={url}******')
            cb_kwargs['city']=self.cities[i] #Passe the current city to Request for the Downloader passe it to the Response.
            yield Request(url, headers=headers, dont_filter=False, cb_kwargs=cb_kwargs)
        logging.debug('End url requests')

    def parse(self, response, city, offset=0):
        '''
        Parses the response.  This method is called by a Scrapy Downloader (not seen in this code).
        Scrapy uses Downloaders to dowloand the response from a request and calls automatically this method.
        '''
        logging.debug('Parse {city} with offset: {offset}')
        headers = {
            'Connection': 'keep-alive',
            'content-type':'application/json',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
            'accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Host': 'www.booking.com',
            #'Referer': f'https://www.booking.com/searchresults.fr.html?lang=fr&ss={city}&offset={offset}',
            }
        
        divs = response.xpath('//div[contains(@data-testid,"property-card")]') # hotels list
        for div in divs:
            url_hotel = div.xpath('descendant::a[contains(@data-testid,"title-link")]/@href').get()
            
            yield{
                'city': city,
                'name' : div.xpath('descendant::div[contains(@data-testid,"title")]/text()').get().strip(),
                'url' :  url_hotel.split('?')[0],
            }
        try:
            # Check if the next button is not disabled, i.e. there is a next page
            button_next = response.xpath('//button[contains(@aria-label,"Page suivante") and not(contains(@class, "dissabled"))]').get()
            if button_next is not None:
                new_offset = offset+25
                url_next_page = f'https://www.booking.com/searchresults.fr.html?lang=fr&ss={city}&offset={new_offset}'
                logging.info(f'Following next page with url: {url_next_page}')
                #headers['Cookie'] = response.headers.getlist('Set-Cookie')
                #logging.info(f'Retrieving next page, cookies:{headers["set-cookie"]}')

                yield response.follow(url_next_page, headers=headers, callback = self.parse, cb_kwargs={'city': city, 'offset': offset+25})
        except (ValueError, KeyError) as noNextKeyError:
            logging.info('There is no next page. The crawling process will terminate:{noNextKeyError}')
            print(f'There is no next page. The crawling process will terminate: {noNextKeyError}')  
    

    def _strip(self, text):
        if text is not None:
            return text.strip()
        return ''
   
    def _extract_first(self, fromtext):
        #Example Re views are defined in a text like this " 23 experiences vecues "
        return self._strip(fromtext).split(' ')[0]
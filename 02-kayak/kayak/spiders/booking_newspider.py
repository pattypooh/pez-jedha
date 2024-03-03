import scrapy
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
from scrapy.utils.log import configure_logging
from kayak.items import HotelItem

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

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': 'True',
        'LOG_LEVEL': 'INFO',
    }
    def __init__(self, cities = None, *args, **kwargs):
        self.cities = cities
        self.start_urls = self._build_start_urls(cities)
        super(NewBookingSpider, self).__init__(*args, **kwargs)

    def _build_start_urls(self, cities: list):
        return [f'https://www.booking.com/searchresults.fr.html?lang=fr&dest_type=city&group_adults=1&no_rooms=1&ss={city}' for city in cities]

    
    def start_requests(self):
        logging.info('1. Starting all url requests')
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
            logging.debug(f'---Starting with url={url}---')
            cb_kwargs['city']=self.cities[i] #Passe the current city to Request for the Downloader passe it to the Response.
            cb_kwargs['offset'] = 0 # For every new city, we restart to 0 
            yield Request(url, headers=headers, dont_filter=False, cb_kwargs=cb_kwargs)
        logging.info('2.End url requests')

    def parse(self, response, city, offset=0):
        '''
        Parses the response.  This method is called by a Scrapy Downloader (not seen in this code).
        Scrapy uses Downloaders to dowloand the response from a request and calls automatically this method.

        Parameters:
        --------------------------------------------------------------------
        city: The city been scrapped
        offset: the latest page offset.  There are 25 hotels per page
        '''
        logging.info(f'Parse {city} with offset: {offset}')
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
            }
        
        divs = response.xpath('//div[contains(@data-testid,"property-card")]') # hotels list
        for div in divs:
            url_hotel = div.xpath('descendant::a[contains(@data-testid,"title-link")]/@href').get()
            url_page = div.xpath('descendant::div[contains(@data-testid,"location")]/a/@href').get()
            
            data = {
                'city': city,
                'name' : div.xpath('descendant::div[contains(@data-testid,"title")]/text()').get().strip(),
                'url' :  url_hotel.split('?')[0],
                'score' : div.xpath('descendant::div[contains(@data-testid, "review-score")]/div/text()').get(),
                'rating_stars': div.xpath('count(descendant::div[contains(@data-testid, "rating-stars")]/span)').get(),
            }
            yield response.follow(url_page, headers=headers, callback= self.parse_hotel, cb_kwargs = {'data': data})
            
        try:
            # Check if the next button is not disabled, i.e. there is a next page
            button_next = response.xpath('//button[contains(@aria-label,"Page suivante") and not(contains(@class, "dissabled"))]').get()
            new_offset = offset+25
            if (button_next is not None and new_offset/25 < 4):#scrap max 4 pages
                url_next_page = f'https://www.booking.com/searchresults.fr.html?lang=fr&dest_type=city&group_adults=1&no_rooms=1&ss={city}&offset={new_offset}'
                logging.info(f'{city}:Following next page with url: {url_next_page}')
                yield response.follow(url_next_page, headers=headers, callback = self.parse, cb_kwargs={'city': city, 'offset': new_offset})
        
        except (ValueError, KeyError) as noNextKeyError:
            logging.info('There is no next page. The crawling process will terminate:{noNextKeyError}')
            print(f'There is no next page. The crawling process will terminate: {noNextKeyError}')  

    def parse_hotel(self, response, data):
        '''
        data: the dictionary containing the previous scrapped data
        '''
        coord_text = response.xpath('//script/text()[contains(.,"b_map_center_latitude")]').get()
        coords = coord_text.split(';')[1:3] # retrieve latitude and longitude, in position 1,2
        data['latitude'] = coords[0].split('=')[1].strip()
        data['longitude'] = coords[1].split('=')[1].strip()
        #logging.info(f'coord_text: {coord_text}')
        yield data
        
       

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
        cities = ["Mont Saint Michel","St Malo","Bayeux","Le Havre","Rouen","Paris","Amiens","Lille","Strasbourg",
          "Chateau du Haut Koenigsbourg","Colmar","Eguisheim","Besancon","Dijon","Annecy","Grenoble","Lyon",
         "Bormes les Mimosas","Cassis","Marseille","Aix en Provence","Avignon","Uzes","Nimes",
          "Aigues Mortes","Saintes Maries de la mer","Collioure","Carcassonne","Ariege","Toulouse","Montauban",
          "Biarritz","Bayonne","La Rochelle"]
        #cities = ["Amiens"]
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
        cb_kwargs = {} # This dict is used to pass more parameters to parse() method
        for i, url in enumerate(self.start_urls):
            print(f'*****starting with url={url}******')
            cb_kwargs['city']=self.cities[i] #Passe the current city to Request for the Downloader passe it to the Response.
            yield Request(url, headers=headers, dont_filter=False, cb_kwargs=cb_kwargs)

    def parse(self, response, city):
        '''
        Parses the response.  This method is called by a Scrapy Downloader (not seen in this code).
        Scrapy uses Downloaders to dowloand the response from a request and calls automatically this method.
        '''
        logging.debug(f'Parsing page for {city}')
        divs = response.xpath('//div[contains(@class,"sr_item_new")]')
        for div in divs:
            data_coords = div.xpath('descendant::a[contains(@class,"bui-link")]/@data-coords').get()
            url_hotel = div.xpath('descendant::a[contains(@class,"bui-link")]/@href').get()
            
            yield{
                'city': city,
                'name' : div.xpath('descendant::span[contains(@class,"sr-hotel__name")]/text()').get().strip(),
                'url' :  url_hotel.split('?')[0],
                'latitude' : data_coords.split(',')[0], #first element is latitude
                'longitude': data_coords.split(',')[1], # second element is longitude
                'desc' : self._strip(div.xpath('descendant::div[contains(@class,"hotel_desc")]/text()').get()),
                'etoiles' : self._extract_first(div.xpath('descendant::span[contains(@class,"bui-rating--smaller")]/@aria-label').get()),
                'note' : self._extract_first(div.xpath('descendant::div[contains(@class,"bui-review-score__badge")]/text()').get()),
                'reviews' : self._extract_first(div.xpath('descendant::div[contains(@class,"bui-review-score__text")]/text()').get()),
            }

        try:
            next_page = response.xpath('//a[contains(@class,"paging-next")]/@href').get()
            logging.info('Retrieving next page')
            yield response.follow(next_page, callback = self.parse, cb_kwargs={'city': city}) 
        except (ValueError, KeyError) as noNextKeyError:
            logging.info('There is no next page. The crawling process will terminate')
            print(f'There is no next page. The crawling process will terminate: {noNextKeyError}')  
    

    def _strip(self, text):
        if text is not None:
            return text.strip()
        return ''
   
    def _extract_first(self, fromtext):
        #Example Re views are defined in a text like this " 23 experiences vecues "
        return self._strip(fromtext).split(' ')[0]
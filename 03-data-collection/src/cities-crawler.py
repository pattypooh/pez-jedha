from urllib import parse
import scrapy
import json
import logging
from scrapy.utils.log import configure_logging


#from scrapy.http import headers

class CityCrawler(scrapy.Spider):
    configure_logging(install_root_handler=False)
    logging.basicConfig(filename='log.txt', format='%(levelname)s: %(message)s%', level=logging.INFO)
    name = 'cityspider'
    #start_urls = ['https://www.booking.com/searchresults.fr.html?lang=fr&ss=Saint+Malo']
    start_urls = ["https://www.booking.com/searchresults.fr.html?lang=fr&ss=Saint+Malo"]

    
    def parse(self, response):
        logging.info('starting parsing')
        #request = scrapy.Request(url, callback=self.parse_js, headers=self.headers)   
        #yield request
        self.parse_hotels(response)
        logging.info(f'{response.status}')
        divs = response.xpath("//div[@class='sr_item']")
        
        with open("./Saint-Malo-scrapy2.html", 'w') as file_obj:
            file_obj.write(response.text)

        logging.info(f'divs= {len(divs)}')
        print("in parse method response = "+ str(response.status))

    def parse_hotels(self, response):
        pass
        
    
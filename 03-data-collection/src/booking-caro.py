# import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

class ParisSpider(Spider):
    name = 'paris'
    allowed_domains = ['booking.com']
    #start_urls = ['https://www.booking.com/searchresults.en-gb.html?lang=en-gb&ss=marseille']
    
    def start_requests(self):
        logger.info('ca commence')

        print('******************************************************************')
        print('ca commence')
        print('******************************************************************')

        opts = Options()
        opts.add_argument(" --headless")
        opts.binary_location = '/usr/bin/google-chrome'

        self.driver = webdriver.Chrome(options=opts, executable_path='/usr/bin/chromedriver')
        print("***** apres webdriver ****")
        self.driver.get('https://www.booking.com/searchresults.en-gb.html?lang=en-gb&ss=marseille')
        title = self.driver.title
        logger.info(title)

        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        logger.info(soup.find_all('div'))

        sel = Selector(text= self.driver.page_source)
        # print('\n')
        # print("je commence")
        # print(self.url)
        # print('\n')
        hotels =  sel.xpath('//div[@class="sr-hotel__title-wrap"]')
        logger.info(f"hotels : {hotels}")
        for hotel in hotels:
            hotel_url = 'https://www.booking.com/' + sel.xpath('//div[@class="sr-hotel__title-wrap"]/..//a/@href').extract_first().replace('\n','')
            hotel_name = sel.xpath('//div[@class="sr-hotel__title-wrap"]/..//a/span/text()').extract()
            hotel_score = sel.xpath('//div[@class="bui-review-score__badge"]/text()').extract()
            # hotel_reviews = sel.xpath('//div[@class="bui-review-score__text"]/text()').extract()
            print('\n')
            print(hotel_url)
            # print(hotel_name)
            # print(hotel_score)
            # print(hotel_reviews)
            # print('\n')
            yield{
                'hotel_url':hotel_url,
                # 'hotel_name':hotel_name,
                # 'hotel_score':hotel_score,
                # 'hotel_reviews':hotel_reviews,
            }
    #     next_page = sel.xpath('//a[@title="Next page"]/@href').extract()
    #     yield Request(next_page, callback=self.parse_next_page)
    def parse_next_page(self, response):
        pass

    def parse(self, response):
        pass
        logger.info("Parsing")
   
filename = "results.csv"
print("*****--main--***********")

        #if filename in os.listdir('src/'):
        #   os.remove('src/' + filename)
process = CrawlerProcess(settings = {
      #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': logging.INFO,
        "FEEDS": {
            '' + filename : {"format": "csv"},
}})

    # Start the crawling using the spider you defined above
process.crawl(ParisSpider)
process.start()





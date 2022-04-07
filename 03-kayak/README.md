## Kayak project

### notebooks/

01-weather.ipynb Retrieves the list of cities, the lat, lon, the weather for the next days<br>
02-hotel-crawler.ipynb Optional use: Calls a python spider to scrap booking.com

### kayak/

I created a spider in the directory spiders.  The python file containing the spider is booking_spider.py<br>
The spider could also be launched using the command line: <br>

> scrapy crawl bookingspy
<br>

### s3/
One notebook is here: 03-botoS3

The files retrieved from API calls and scrapping were saved in aws S3<br>
ETL: 2 tables were created (city and hotel) in AWS RDS.  Data from scrapped files was processed save in the database using SQLAlchemy

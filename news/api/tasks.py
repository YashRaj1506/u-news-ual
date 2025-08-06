# import os

# from celery import shared_task
# from api.webscraper import scraper
# import time

# from api.webscraper.scraper import scrape_news_indiatoday_func, scrape_news_nytimes_func, scrape_news_livemint_func

# from api.webscraper.helper_functions import create_superuser, flush_database


# @shared_task(bind=True)
# def test_not_func(self):
#     # operations
#     for i in range(10):
#         print(i)
#     return "Done"

# @shared_task(bind=True)
# def test_func(self):

#     flush_database()

#     time.sleep(1)

#     create_superuser(os.getenv('SUPERUSER_NAME'), os.getenv('SUPERUSER_EMAIL'), os.getenv('SUPERUSER_PASSWORD'))

#     time.sleep(1)

#     scrape_news_indiatoday_func('https://www.indiatoday.in/rss/1206550', 'sports')
#     time.sleep(1)
#     scrape_news_indiatoday_func('https://www.indiatoday.in/rss/1206513', 'economy')
#     time.sleep(1)
#     scrape_news_indiatoday_func('https://www.indiatoday.in/rss/1206577', 'world')
#     time.sleep(1)
#     scrape_news_indiatoday_func('https://www.indiatoday.in/rss/1206504', 'society&arts')
#     time.sleep(1)
#     scrape_news_indiatoday_func('https://www.indiatoday.in/rss/1206514', 'politics')
#     time.sleep(1)

#     # scrape_news_nytimes_func('https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml', 'politics')
#     # time.sleep(1)
#     # scrape_news_nytimes_func('https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml', 'sports')
#     # time.sleep(1)
#     # scrape_news_nytimes_func('https://rss.nytimes.com/services/xml/rss/nyt/Science.xml', 'science')
#     # time.sleep(1)
#     # scrape_news_nytimes_func('https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml', 'environment')
#     # time.sleep(1)
#     # scrape_news_nytimes_func('https://rss.nytimes.com/services/xml/rss/nyt/Space.xml', 'space')
#     # time.sleep(1)

#     scrape_news_livemint_func('https://www.livemint.com/rss/sports','sports')
#     time.sleep(1)
#     scrape_news_livemint_func('https://www.livemint.com/rss/politics','politics')
#     time.sleep(1)
#     scrape_news_livemint_func('https://www.livemint.com/rss/money','economy')
#     time.sleep(1)
#     scrape_news_livemint_func('https://www.livemint.com/rss/science','science')
#     time.sleep(1)
#     scrape_news_livemint_func('https://www.livemint.com/rss/education','Education')
#     time.sleep(1)
#     return "Done"

import os
import time
from celery import shared_task, group
from api.webscraper.scraper import (
    scrape_news_indiatoday_func,
    scrape_news_nytimes_func,
    scrape_news_livemint_func
)
from api.webscraper.helper_functions import create_superuser, flush_database

@shared_task(bind=True)
def test_not_func(self):
    for i in range(10):
        print(i)
    return "Done"

@shared_task
def scrape_indiatoday(url, category):
    scrape_news_indiatoday_func(url, category)

@shared_task
def scrape_nytimes(url, category):
    scrape_news_nytimes_func(url, category)

@shared_task
def scrape_livemint(url, category):
    scrape_news_livemint_func(url, category)

@shared_task(bind=True)
def test_func(self):
    """Main scheduled Celery task that runs all scraping tasks in parallel."""

    # Flush database before scraping
    flush_database()
    time.sleep(1)

    # Create superuser
    create_superuser(
        os.getenv('SUPERUSER_NAME'), 
        os.getenv('SUPERUSER_EMAIL'), 
        os.getenv('SUPERUSER_PASSWORD')
    )
    time.sleep(1)

    # Define tasks as a Celery group for parallel execution
    scraping_tasks = group([
        scrape_indiatoday.s('https://www.indiatoday.in/rss/1206550', 'sports'),
        scrape_indiatoday.s('https://www.indiatoday.in/rss/1206513', 'economy'),
        scrape_indiatoday.s('https://www.indiatoday.in/rss/1206577', 'world'),
        scrape_indiatoday.s('https://www.indiatoday.in/rss/1206504', 'society&arts'),
        scrape_indiatoday.s('https://www.indiatoday.in/rss/1206514', 'politics'),

        # scrape_nytimes.s('https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml', 'politics'),
        # scrape_nytimes.s('https://rss.nytimes.com/services/xml/rss/nyt/Sports.xml', 'sports'),
        # scrape_nytimes.s('https://rss.nytimes.com/services/xml/rss/nyt/Science.xml', 'science'),
        # scrape_nytimes.s('https://rss.nytimes.com/services/xml/rss/nyt/Climate.xml', 'environment'),
        # scrape_nytimes.s('https://rss.nytimes.com/services/xml/rss/nyt/Space.xml', 'space'),

        scrape_livemint.s('https://www.livemint.com/rss/sports', 'sports'),
        scrape_livemint.s('https://www.livemint.com/rss/politics', 'politics'),
        scrape_livemint.s('https://www.livemint.com/rss/money', 'economy'),
        scrape_livemint.s('https://www.livemint.com/rss/science', 'science'),
        scrape_livemint.s('https://www.livemint.com/rss/education', 'education')
    ])

    # Execute all tasks in parallel
    scraping_tasks.apply_async()

    return "Scraping tasks started in parallel!"

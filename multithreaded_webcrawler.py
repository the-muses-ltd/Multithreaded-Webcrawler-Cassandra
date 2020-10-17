# This is a reusable webcraawler architecture that can be adapted to scrape any webstie.

# RESULTS:
# Roughly 24 seconds per thousand courses scraped for ThreadPoolExecutor vs 63s for unthreaded script.
# This is a very basic implementation of multithreading in order to show the proof of concept, but is a good base to build off of.

import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
import time
import logging
from mitopencourseware_crawler_worker import mit_crawler


def courses_spider(max_pages):
    data_to_csv = [] #holds all data to send to csv
    print("Webcrawler workers have started, please wait while we finish crawling...") 

    # remove max pages loop (unecessary)
    page = 1
    while page <= max_pages:
        url = 'https://ocw.mit.edu/courses/'
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        # Multithread only the work:
        # Tuning is required to find the most efficient amount of workers in the thread pool.
        with ThreadPoolExecutor(max_workers=30) as executor:
            start = time.time()
            futures = [ executor.submit(work, link) for link in soup.findAll('h4', {'class': 'course_title'}, limit=100) ]
            data_to_csv = []
            for result in as_completed(futures):
                data_to_csv.append(result.result())
            end = time.time()
            print("Time Taken to complete: {:.6f}s".format(end-start))
            print("Courses extracted: ", len(data_to_csv))
        page += 1
    export_to_csv(data_to_csv)

def work(link):
    # replace this fucntion with the specific crawler you want to use:
    return mit_crawler(link)


# Exports data to a formatted csv file, this will be replaced with multithreaded API calls to the Cassandra Prisma Database 
# or on the cloud in production, it will be sent to the S3 temporary database to be picked up by the AWS Lambda funtion which will push it to the Cassandra Database
def export_to_csv(csv_data):
    with open('web_crawl_data.csv',mode='w') as csv_file:
        field_names = ['Title','URL extension','External Website Logo','URL(href)','Description','Course logo URL']
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)#delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        csv_writer.writeheader()
        for course in csv_data:
            course_data = {
                'Title':course[0],
                'URL extension':course[1],
                'External Website Logo':course[2],
                'URL(href)':course[3],
                'Description':course[4],
                'Course logo URL':course[5],
            } 
            csv_writer.writerow(course_data)
            



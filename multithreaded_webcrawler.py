# RESULTS:
# Roughly 24 seconds per thousand courses scraped for ThreadPoolExecutor vs 63s for unthreaded script.
# This is a very basic implementation of multithreading in order to show the proof of concept, but is a good base to build off of.

import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
import time
import logging


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
            futures = [ executor.submit(work, link) for link in soup.findAll('h4', {'class': 'course_title'}, limit=1000) ]
            data_to_csv = []
            for result in as_completed(futures):
                data_to_csv.append(result.result())
            end = time.time()
            print("Time Taken to complete: {:.6f}s".format(end-start))
            print("Courses extracted: ", len(data_to_csv))
        page += 1
    export_to_csv(data_to_csv)

def work(link):
    link_title = link.find('a', {'rel': 'coursePreview'})
    href = 'https://ocw.mit.edu' + link_title.get('href')

    #need to get rid of whitespace in title
    title = cut_white_spaces(link_title.string)

    url_extension = href.split('/')[4]
    logo = 'https://scontent.fcpt3-1.fna.fbcdn.net/v/t31.0-8/10505138_10152190076601857_3373879292029985409_o.png?_nc_cat=107&_nc_ohc=Zra5A8DAAHgAQnslCxM1jIYUWdc9c8F42YVgFCFoh-kHaQCV50CAen1TA&_nc_ht=scontent.fcpt3-1.fna&oh=e8fae2fc323cf025b62a968bc13469f7&oe=5E7B6266'
            
    return_data = get_single_course_data(href)
    course_data = [title,url_extension,logo,href]
    course_data = course_data + return_data #concat data from function call and current function
    return course_data

def get_single_course_data(item_url):
    return_data = []
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for item_description in soup.findAll('div', {'id': 'description'}):
        description = item_description.findAll('p')
        entire_description = ''
        for p in description:
            if p.string != None:
                entire_description += p.string
        return_data.append(entire_description)
    for logo_url in soup.findAll('img', {'itemprop': 'image'}):
        return_data.append(('https://ocw.mit.edu' + logo_url.get('src')))
    return return_data



#large amount of whitespace between the course title and the year, so cut all that out
def cut_white_spaces(title):
    title = title.strip() #strip trailing/leading whitespace
    index = title.find('(')
    course_name = title[:index].strip()
    course_year = title[index:]
    return ("%s %s" % (course_name,course_year))

#exports data to a formatted csv file
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
            



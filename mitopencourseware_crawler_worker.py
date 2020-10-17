import requests
from bs4 import BeautifulSoup

def mit_crawler(link):
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


#large amount of whitespace between the course title and the year, so cut all that out
def cut_white_spaces(title):
    title = title.strip() #strip trailing/leading whitespace
    index = title.find('(')
    course_name = title[:index].strip()
    course_year = title[index:]
    return ("%s %s" % (course_name,course_year))

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
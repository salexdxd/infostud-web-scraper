import requests
from bs4 import BeautifulSoup
import pandas as pd

#TODO
# Acces webside using requests
# Parse data using BeautifulSoup4
    # Get name of the company
    # Get job name
    # Get date of announcement
    # Get Location
    # Get URL
# Convert data into Pandas Dataframe
# Save data as .csv file
# Every .csv file saves data in format: Company name, Job name, date, Location, URL



def pages():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    url_search = 'Data-Science'
    url_page = f'https://poslovi.infostud.com/oglasi-za-posao-{url_search}/beograd?category%5B0%5D=5&dist=50&esource=homepage'
    response=requests.get(url_page, headers=headers)
    doc = BeautifulSoup(response.text, 'lxml')
    if response.status_code != 200:
        raise Exception('Error while loading {}'.format(url_page))
    page_number = doc.find_all('ul', class_= 'uk-pagination uk-flex-center')
    total_pages = 0
    for i in page_number:
        page = i.find_all('li')[-2]
        page=int(page.text.strip())
        total_pages=page
    return total_pages



def content(num):

    content_list=[]
    for x in range(1, num+1):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        search = 'Data-Science'
        url = f'https://poslovi.infostud.com/oglasi-za-posao-{search}/beograd?category%5B0%5D=5&dist=50&page={x}'
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise Exception(f'Error while loading {url}')
        soup = BeautifulSoup(r.text, 'lxml')
        content_list.append(soup)
    content_list = str(content_list)
    all_content = BeautifulSoup(content_list, 'lxml')
    return all_content


def company_name(doc):
    list_of_comp_names=[]
    comp_find = doc.find_all('p', class_='uk-h4 uk-margin-remove')
    for n in comp_find:
        n=n.text.strip()
        list_of_comp_names.append(n)
    return list_of_comp_names

def location(doc):
    list_of_locations=[]
    loc_find = doc.find_all('p', class_='uk-margin-remove-bottom')
    for j in loc_find:
        j=j.text.strip()
        list_of_locations.append(j)
    return list_of_locations

def release_date(doc):
    list_of_dates=[]
    date_find = doc.find_all('p', class_='uk-margin-remove uk-text-bold')
    for v in date_find:
        v=v.text.strip()
        list_of_dates.append(v)
    return list_of_dates


def link(doc):
    base_url = 'https://poslovi.infostud.com'
    list_of_links=[]
    link_find = doc.find_all('h2', class_=['uk-h3 uk-margin-remove-bottom uk-text-break', 'uk-h3 uk-margin-remove-bottom uk-text-break job__title_no_logo', 'uk-h3 uk-margin-remove-bottom job__title_no_logo uk-text-break'])
    for link in link_find:
        for l in link.find_all('a', href=True):
            list_of_links.append(base_url + l['href'])
    return list_of_links

def job_name(doc):
    list_of_jobs=[]
    job_find = doc.find_all('h2', class_=['uk-h3 uk-margin-remove-bottom uk-text-break', 'uk-h3 uk-margin-remove-bottom uk-text-break job__title_no_logo', 'uk-h3 uk-margin-remove-bottom job__title_no_logo uk-text-break'])
    for n in job_find:
        n=n.text.strip()
        list_of_jobs.append(n)
    return list_of_jobs



def main(doc):#main
    main_dict = {
        'Company Name': company_name(doc),
        'Job Name': job_name(doc),
        'Location': location(doc),
        'Date': release_date(doc),
        'URL': link(doc)
    }
    df = pd.DataFrame(main_dict)
    #df.to_csv('infostud-scraper.csv', index=None)
    return df




nums = pages()
document = content(nums)
test = main(document)
#print(test)




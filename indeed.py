import requests
from bs4 import BeautifulSoup
import time
import random  
LIMIT = 50
URL = f'https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&vjk=6a7446eb57ad8e77&limit={LIMIT}'
INDEED_URL = 'https://kr.indeed.com'
# start 포함 url
# https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit=50&start=0&vjk=a515eccaec90411f

def extract_indeed_pages():
    # indeed에서 python 검색결과 페이지에서 최대 페이지 수 추출
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    # time.sleep(2)
    pagination = soup.find('div', {'class' : 'pagination'})  
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    
    return max_page 

def extract_job(html):
    # title, company, anchor 추출
    # time.sleep(2)
    title = html.find('h2', {'class' : 'jobTitle'}).find('a')['aria-label']
    # print(f'title : {title[:-10]}')
    company = html.find('span', {'class' : 'companyName'}).string
    # print(f'company : {company}')
    anchor = html.find('h2', {'class' : 'jobTitle'}).find('a')['href']
    # print(f'anchor : {INDEED_URL}{anchor}')
    location = html.find('div', {'class' : 'companyLocation'}).string

    return {'title' : title[:-10], 'company' : company, 'location' : location, 'anchor' : INDEED_URL + anchor} #  

def extract_indeed_jobs(last_page):
    # 모든 페이지에서 job 정보 추출
    jobs = []
    for page in range(last_page):
        result = requests.get(f'{URL}&start={1*LIMIT}')
        # time.sleep(2)
        soup = BeautifulSoup(result.text, 'html.parser')
        # time.sleep(2)

        results = soup.find_all('table', {'class' : 'jobCard_mainContent'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

    
import requests
import asyncio

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from natsort import natsorted
from datetime import datetime

i = 1
repeated_link = ''

def make_jobs(soup, jobs, page_number) :
    """A function to parse html page and make a dictionary containing jobs"""
    global i
    global repeated_link

    for link in soup.find_all('a') :
        job_link = link.get('href')
    
        if "magnet/jobs/" in job_link and link.text and f"https://quera.ir/{job_link}" not in repeated_link :
            jobs[f"page={page_number}-{i}-{link.text}"] = [f"https://quera.ir/{job_link}", link.text, page_number]
            # add link to user links to prevent repeat
            repeated_link += f"https://quera.ir/{job_link}"
            i = i + 1    

async def get_object(page_number, key_length, key, session, jobs) :
    """A function to get the page response, according to the page number"""

    if key_length == 0 :
        response = await session.request(method='GET', url= f"https://quera.ir/magnet/jobs?page={page_number}")
    if key_length == 1 :
        response = await session.request(method='GET', url= f"https://quera.ir/magnet/jobs/{key}?page={page_number}")
    if key_length > 1 :
        response = await session.request(method='GET', url= f"https://quera.ir/magnet/jobs?{key}&page={page_number}")
        
    make_jobs((BeautifulSoup(await response.read(), 'html.parser')), jobs, page_number)

async def main(keyword) :
    """Main function"""
    time1 = datetime.now()

    print("*****************************************")
    jobs = {}
    url = "https://quera.ir/magnet/jobs"

    keyword = keyword.replace("c#", "c%23")
    keyword = keyword.replace('react', 'reactjs')

    # Calculate how many words does key have
    key_words = keyword.split()   

    key_length = len(key_words)
    # First response to see if results are more than one page
    
    # If key_length is equal to 0
    if key_length == 0:
        response = requests.get(url)

    # If key_length is equal to 1
    if key_length == 1 :
        response = requests.get(f"{url}/{key_words[0]}")    

    # If key_length is bigger than 1
    elif key_length > 1 :
        keyword = ''
        for word in key_words :
            keyword += f"technologies={word}&"        
        keyword = keyword[:-1]
        response = requests.get(f"{url}?{keyword}")

    soup = BeautifulSoup(response.text, 'html.parser')
    html_page_amount = len(soup.find_all(class_="chakra-button css-15wculr"))

    # If the amount of page counters in html is 0, amount of pages is equal to 1
    if html_page_amount == 0 :
        print(1)
        make_jobs(soup, jobs, 1)

    # If the amount of page counters in html isn't 0,
    # Real amount of pages is equal to [html_page_amount - 1]
    else :
        page_amount = int(soup.find_all(class_="chakra-button css-15wculr")[html_page_amount - 2].text)

        async with ClientSession() as session :
            await asyncio.gather( *[get_object(page_number, key_length, keyword, session, jobs) for page_number in range(1, page_amount + 1)] )

    final_jobs = {}
    for key in natsorted(jobs.keys()) :
            final_jobs[key] = jobs[key]
            print('page = ', jobs[key][2], ' - ', jobs[key][1], ' - ', jobs[key][0])

    time2 = datetime.now()  
    print(len(list(jobs.items())))
    print(f"Time = {time2 - time1}")  

    return final_jobs

def run_program(keyword):
    """Run the whole file"""
    # Windows requirement to run the async Function(Not needed in linux based systems !)
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    jobs_string = asyncio.run(main(keyword))
    
    global i
    i = 0
    global repeated_link
    repeated_link = ''

    return jobs_string


run_program("python")
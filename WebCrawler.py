import requests
from bs4 import BeautifulSoup
import re
import sys
import concurrent.futures

MAX_THREADS = 30
crawled = []
errors = []

def search_links(urlvalue):
    return_links = []
    r = requests.get(urlvalue, headers={"User-Agent": "TestUser"})

    soup = BeautifulSoup(r.content, "lxml")

    if r.status_code != 200:
        errors.append(urlvalue)
        return "Error"
    else:
        crawled.append(urlvalue)
        for linkvalue in soup.findAll('a', attrs={'href': re.compile("^http")}):
            if linkvalue.get('href') not in crawled :
                return_links.append(linkvalue.get('href'))
    print (urlvalue)
    for i in return_links:
        print(" "*4 + i)
    return return_links

def web_crawl(link):
    return_urls = search_links(link)
    threads = min(MAX_THREADS, len(link))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(search_links, return_urls)
    print(str(len(crawled)) + " website(s) crawled without errors.")
    print(str(len(errors)) + " website(s) with errors.")
    
web_crawl(sys.argv[1])
    
import requests
from bs4 import BeautifulSoup
import re
import sys
import concurrent.futures

MAX_THREADS = 30
crawled = []

def search_links(urlvalue):
    crawled.append(urlvalue)
    return_links = []
    r = requests.get(urlvalue)

    soup = BeautifulSoup(r.content, "lxml")

    if r.status_code != 200:
        return "Error"
    else:
        for linkvalue in soup.findAll('a', attrs={'href': re.compile("^http")}):
            if linkvalue.get('href') not in crawled :
                return_links.append(linkvalue.get('href'))
            #if len(return_links) == 10:
             #   break
    print (urlvalue)
    for i in return_links:
        print(" "*4 + i)
    return return_links

def web_crawl(link):
    return_urls = search_links(link)
    threads = min(MAX_THREADS, len(link))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(search_links, return_urls)
    print(str(len(crawled)) + " websites crawled without errors.")
    
web_crawl(sys.argv[1])
    
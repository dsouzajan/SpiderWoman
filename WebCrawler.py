import requests
from bs4 import BeautifulSoup
import re
import sys
import concurrent.futures

#initial variables
MAX_THREADS = 30
crawled = []
errors = []

#function to scrape url and print 
def search_links(urlvalue):
    return_links = [] #output list
    
	#get xml and html data from url
	r = requests.get(urlvalue, headers={"User-Agent": "TestUser"})
	soup = BeautifulSoup(r.content, "lxml")

    #look and check for href links and error out if status code is not OK
	if r.status_code != 200:
        errors.append(urlvalue)
        return "Error"
    else:
        crawled.append(urlvalue)
        for linkvalue in soup.findAll('a', attrs={'href': re.compile("^http")}):
            if linkvalue.get('href') not in crawled :
                return_links.append(linkvalue.get('href'))
				
    #print out expected output and return urls for next url scraping
	print (urlvalue)
    for i in return_links:
        print(" "*4 + i)
    return return_links

#main web crawl function
def web_crawl(link):
	#run function once to get first set of urls
    return_urls = search_links(link)
	
	#use threading to loop through next urls
    threads = min(MAX_THREADS, len(link))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(search_links, return_urls)
		
	#print totals
    print(str(len(crawled)) + " website(s) crawled without errors.")
    print(str(len(errors)) + " website(s) with errors.")
    
web_crawl(sys.argv[1])
    
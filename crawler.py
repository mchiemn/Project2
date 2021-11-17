from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import random
import time
import re   
import cchardet


class page:
    def __init__(self, outlinks):
        self.outlinks = outlinks
        self.outlinksList = []

def scrapeCPP():
    content = requests.get('https://www.cpp.edu/').content
    # Minimum number of links to crawl
    crawled = 0
    target = 2

    # Set of links we could crawl
    set_of_outlinks = set(())

    # Dictionary stores all the links that we have crawled
    # Key = URL, Value = page object
    linksCrawled = {'https://www.cpp.edu/' : 0}

    start = time.time()
    while crawled < target:
        # Create new page object for the page we are crawling
        newPage = page(0)

        # Crawl through the page and only get links that are 'cpp.edu'
        for link in BeautifulSoup(content, parse_only = SoupStrainer('a', href=re.compile('cpp.edu/')), features='lxml'):
            if hasattr(link, 'href') and link['href'].startswith('https'):
                # Increase number of outlinks
                # This will probably change so that it only contains number of outlinks
                # within the linksCrawled dictionary
                newPage.outlinks += 1

                # If the link we find is not already crawled, add it to the set of possible links we can crawl
                if(link['href'] not in linksCrawled):
                    set_of_outlinks.add(link['href'])
                
                # Change this to a dictionary for fast lookup instead of list
                # key is link, value is just index (value doesnt matter)
                newPage.outlinksList.append(link['href'])

        # If the set of links we can crawl is empty, then stop crawling
        if len(set_of_outlinks) == 0:
            break
        
        while True:
            try:
                # Get new link from set of outlinks and set content for next loop
                newLink = random.choice(list(set_of_outlinks))
                list(set_of_outlinks).remove(newLink)
                content = requests.get(newLink).content
            except requests.exceptions.ConnectionError:
                continue
            break

        # Update the dictionary
        if crawled == 0: # If the page crawled is the first one
            linksCrawled.update({'https://www.cpp.edu/' : newPage})
        # Key = URL of next page we will crawl
        # Value = page Object
        else:
            linksCrawled.update({newLink : newPage})
        crawled += 1

        # Time between each crawl so we don't get banned
        time.sleep(1.5)
    end = time.time()

    for key, value in linksCrawled.items():
        print(key, value.outlinks)
    print(end - start)




def main():
    time_start = time.time()
    scrapeCPP()
    time_end = time.time()
    print('Time elapsed: ' + str(time_end - time_start) + ' sec')

    # time_start = time.time()
    # scrape('https://www.20minutes.fr/', 'fr')               # french
    # time_end = time.time()
    # print('Time elapsed: ' + str(time_end - time_start) + 'sec')

    # time_start = time.time()
    # scrape('https://elpais.com/america/', 'es')               # spanish
    # time_end = time.time()
    # print('Time elapsed: ' + str(time_end - time_start) + 'sec')


if __name__ == '__main__':
    main()
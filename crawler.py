from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
import random
import time
import re
import cchardet

# Page objects
# Uses dictionary for O(1) lookup when calculating pagerank


class page:
    def __init__(self, outlinks=0, pagerank=0):
        self.outlinks = outlinks
        self.pagerank = pagerank
        self.outlinksDict = {}


def scrapeCPP():
    # Minimum number of links to crawl
    crawled = 0
    target = 20

    # Set of links we could crawl
    set_of_outlinks = set(())

    # Dictionary stores all the links that we have crawled
    # Key = URL, Value = page object
    linksCrawled = {'https://www.cpp.edu/index.shtml': 0}

    start = time.time()
    while len(linksCrawled) < target:

        if crawled == 0:
            content = requests.get('https://www.cpp.edu/index.shtml').content
        else:
            while True:
                try:
                    # Get new link from set of outlinks and set content for next loop
                    newLink = random.choice(list(set_of_outlinks))
                    set_of_outlinks.remove(newLink)
                    content = requests.get(newLink).content
                except requests.exceptions.ConnectionError:
                    continue
                break
        # Create new page object for the page we are crawling
        newPage = page()

        # Counter variable that only serves to create the page object's dictionary
        counter = 0
        # Crawl through the page and only get links that are 'cpp.edu'
        for link in BeautifulSoup(content, parse_only=SoupStrainer('a', href=re.compile('cpp.edu/')), features='lxml'):
            if hasattr(link, 'href') and link['href'].startswith('https'):
                # Increase number of outlinks
                # This will probably change so that it only contains number of outlinks
                # within the linksCrawled dictionary
                newPage.outlinks += 1

                # If the link we find is not already crawled, add it to the set of possible links we can crawl
                if(link['href'] not in linksCrawled):
                    set_of_outlinks.add(link['href'])

                # Add the link to the page object's dictionary
                newPage.outlinksDict.update({link['href']: counter})

        # Update the dictionary
        if crawled == 0:  # If the page crawled is the first one
            linksCrawled.update({'https://www.cpp.edu/index.shtml': newPage})
        # Key = URL of next page we will crawl
        # Value = page Object
        else:
            linksCrawled.update({newLink: newPage})

        # Update number crawled
        crawled += 1
        print(len(linksCrawled))

        # If the set of links we can crawl is empty, then stop crawling
        # If the number of crawled links reaches our target, then stop crawling
        if len(set_of_outlinks) == 0 or len(linksCrawled) == target:
            break

        # Time between each crawl so we don't get banned
        time.sleep(1.5)
    end = time.time()

    # Recursive method to remove links not crawled AND remove links with no outlinks
    removeLinks(linksCrawled)

    # After removal of links, initialize page rank values for each object
    for value in linksCrawled.values():
        value.pagerank = 1 / len(linksCrawled)

    '''# Prints the link, the number of outlinks it has, and what those outlinks are
    # Comment out for large crawls please
    for key, value in linksCrawled.items():
        print(key, value.outlinks, value.pagerank)
        #Print to see what links the page outlinks to
        #for outlink in value.outlinksDict.keys():
            #print(outlink)'''

    return linksCrawled


def removeLinks(linksCrawled):
    hasDanglingLink = False
    for key, value in list(linksCrawled.items()):
        currentDict = value.outlinksDict
        # For each key in the page's outlink dictionary
        for objKey in list(currentDict.keys()):
            # If that key is a URL we have not crawled, remove it
            if objKey not in linksCrawled:
                del value.outlinksDict[objKey]
        # Update number of outlinks for this page object
        value.outlinks = len(value.outlinksDict)
        # Remove the link from the dict if it has no outlinks
        if value.outlinks == 0:
            del linksCrawled[key]
            hasDanglingLink = True
    if hasDanglingLink:
        removeLinks(linksCrawled)

    return linksCrawled


def get_cpp_dict():
    return scrapeCPP()

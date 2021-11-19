import wikipedia
import random
import time
import csv

KEY_TERM = 'Characters of the Marvel Cinematic Universe'
TARGET = 1000
FILE_OUT = 'data/marvel/wiki-repo.csv'
FILE_FILTER = 'data/marvel/wiki-repo-filtered.csv'
FILE_FINAL = 'data/marvel/wiki-repo-final.csv'


# Assumes argument outlinks is a list provided by wikipedia api
# or empty list for pages with no outlinks
class PageOutlinks:
    def __init__(self, outlinks):
        self.outlinks_li = outlinks
        self.outlinks = len(outlinks)
        # removes commas for .CSV consistency
        for i in range(0, len(outlinks)):
            self.outlinks_li[i] = self.outlinks_li[i].replace(',', ' ')


# Builds a dictionary from .csv file
def build_list(file):
    link_dict = {}
    with open(file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, skipinitialspace=True)
        for row in csv_reader:
            # remove trailing comma from .csv
            row.remove(row[-1])
            # convert outlinks to int
            row[1] = int(row[1].replace('\'',''))

            # create empty page object
            new_page = PageOutlinks([])
            if row[1] != 0:
                for i in row[2:]:
                    # add outlinks as dictionary entries with value 0
                    new_page.outlinks_li.append(i)
                # update number of outlinks
                new_page.outlinks = row[1]
            # add page object to new dictionary
            link_dict[row[0]] = new_page
    return link_dict


# Converts list of outlinks into a CSV string, then writes data to file
def write_to_file(filename, links_dict):
    # creates list of dictionary keys
    dict_keys = list(links_dict.keys())

    # creates first line - overwrites existing data
    outlinks_str = ''
    if links_dict[dict_keys[0]].outlinks != 0:
        for i in links_dict[dict_keys[0]].outlinks_li:
            outlinks_str += i + ', '
    with open(filename, 'w') as f:
        f.write('%s,%s,%s\n' % (dict_keys[0], links_dict[dict_keys[0]].outlinks, outlinks_str))

    # appends remaining lines
    for i in range(1, len(links_dict)):
        outlinks_str = ''
        if links_dict[dict_keys[i]].outlinks != 0:
            for j in links_dict[dict_keys[i]].outlinks_li:
                outlinks_str += j + ', '
        with open(filename, 'a') as f:
            f.write('%s,%s,%s\n' % (dict_keys[i], links_dict[dict_keys[i]].outlinks, outlinks_str))


# removes outlinks that do not point to any indexes
def strip_dict(outlinks_dict):
    dict_keys = list(outlinks_dict.keys())
    new_dict = {}

    # iterates through dictionary
    for i in range(0, len(outlinks_dict)):
        active_links =[]
        # iterates though all links
        for j in outlinks_dict[dict_keys[i]].outlinks_li:
            if j in dict_keys:
                active_links.append(j)
        # creates new object with only relevant outlinks
        new_page = PageOutlinks(active_links)
        # adds truncated entry to dictionary
        new_dict[dict_keys[i]] = new_page
    return new_dict


# removes indexes with no outlinks and with no inlinks
# !!call only after using strip_dict first
def truncate_dict(outlinks_dict):
    dict_keys = list(outlinks_dict.keys())
    new_dict ={}

    for i in range(0, len(outlinks_dict)):
        for j in range(0, len(outlinks_dict)):
            if dict_keys[i] in outlinks_dict[dict_keys[j]].outlinks_li:
                new_dict[dict_keys[i]] = outlinks_dict[dict_keys[i]]
                break
    return new_dict


def scrape_wiki():
    # Minimum number of links to crawl
    crawled = 0
    target = TARGET

    # Dictionary stores all the links that we have crawled
    # Key = URL, Value = WikiOutlinks object
    links_crawled = {}

    # Set of links we could crawl
    set_of_outlinks = set(())

    # Initial key term
    search_term = KEY_TERM
    try:
        wiki = wikipedia.page(KEY_TERM)
    except wikipedia.exceptions.PageError as e:
        li = wikipedia.search(search_term, 2)
        try:
            wiki = wikipedia.page(li[0])
            # try to parse data in first search result
        except wikipedia.exceptions.DisambiguationError:
            wiki = wikipedia.page(li[1])
        # if the first search result is too vague, the parser will return an error
        # so, the second result is selected (see Wikipedia API documentation)
    print("Search: " + wiki.title)

    # Build set - Assumes initial search contains a large amount of outlinks
    # Here, we begin with a Wiki category
    set_of_outlinks.update(wiki.links)
    print("Set size: " + str(len(set_of_outlinks)))

    # Begin crawl:
    while crawled < target:
        print('Wikipage retrieved: ' + wiki.title)
        title_str = wiki.title.replace(',', ' ')

        # Check if page contains outlinks:
        print('Crawled: ' + str(len(links_crawled)) + '\t\tOutlinks:', end=' ')
        try:
            print(str(len(wiki.links)))
        except KeyError as e:
            print('No outlinks available')
            new_page = PageOutlinks([])
            links_crawled[title_str] = new_page
            crawled += 1

        # Add to dictionary:
        if wiki.title not in links_crawled:
            new_page = PageOutlinks(wiki.links)
            # 'links' method returns a list of internal links parsed from the page
            # new_page constructs a WikiOutlinks object with a list argument
            links_crawled[title_str] = new_page
            # new_page is added to links_crawled dictionary
            crawled += 1

        # Select a new link to crawl:
        search_term = random.choice(list(set_of_outlinks))
        print("Search: " + search_term)
        new_term = False
        while not new_term:
            try:
                wiki = wikipedia.page(search_term)
                new_term = True
            except wikipedia.exceptions.PageError:
                li = wikipedia.search(search_term)
                search_term = random.choice(li)
            except wikipedia.exceptions.DisambiguationError:
                li = wikipedia.search(search_term)
                search_term = random.choice(li)
            except wikipedia.exceptions.HTTPTimeoutError:
                print("!!Timeout Error")
                time.sleep(5)
                # timeout error
            except wikipedia.exceptions.WikipediaException:
                print("!!Timeout Error")
                time.sleep(5)
                # timeout error
        time.sleep(1)

    # remove unneeded links from matrix
    write_to_file(FILE_OUT, links_crawled)
    links_reduced = strip_dict(links_crawled)
    write_to_file(FILE_FILTER, links_reduced)
    links_final = truncate_dict(links_reduced)
    write_to_file(FILE_FINAL, links_final)


def main():
    time_start = time.time()
    scrape_wiki()
    time_end = time.time()
    print('Time elapsed: ' + str(time_end - time_start) + ' sec')


if __name__ == '__main__':
    main()
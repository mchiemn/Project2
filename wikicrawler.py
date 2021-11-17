import wikipedia
import random
import time


class Page:
    def __init__(self, outlinks):
        self.outlinks = len(outlinks)
        self.outlinks_dict = {}
        for i in outlinks:
            self.outlinks_dict[i] = 0


def scrape_wiki():
    # Minimum number of links to crawl
    crawled = 0
    target = 10

    # Dictionary stores all the links that we have crawled
    # Key = URL, Value = Page object
    links_crawled = {}

    # Set of links we could crawl
    set_of_outlinks = set(())

    # Initial key term
    key_term = 'Tropical fish'
    search_term = key_term

    # Begin crawl
    while crawled < target:
        li = wikipedia.search(search_term, 2)
        # returns a list of relevant terms in the Wiki database
        try:
            wiki = wikipedia.page(li[0])
            # try to parse data in first search result
        except wikipedia.exceptions.DisambiguationError as e:
            wiki = wikipedia.page(li[1])
            # if the first search result is too vague, the parser will return an error
            # so, the second result is selected (see Wikipedia API documentation)
        except wikipedia.exceptions.PageError as e:
            li = wikipedia.search(key_term, 2)
            try:
                wiki = wikipedia.page(li[0])
            except wikipedia.exceptions.DisambiguationError as e:
                wiki = wikipedia.page(li[1])
            # restarts search if null search i.e. a Wikipedia page on
            # search term does not yet exist (rare)

        print('Page: ' + wiki.title)
        #print('Outlinks: ' + str(len(wiki.links)))
        print('Crawled: ' + str(len(links_crawled)))
        new_page = Page(wiki.links)
        # 'links' function a list of internal links parsed from the page

        # Add to dictionary
        if wiki.title not in links_crawled:
            for a in wiki.links:
                if a not in set_of_outlinks:
                    set_of_outlinks.add(a)

            links_crawled[wiki.title] = new_page
            crawled += 1

        if len(set_of_outlinks) == 0:
            break

        # Select link to crawl
        search_term = random.choice(list(set_of_outlinks))
        time.sleep(1.5)

    #
    # Sample output:
    #
    print("SAMPLE OUTPUT")
    print(len(links_crawled))
    for i in links_crawled:
        print(i + ' - outlinks: ' + str(links_crawled[i].outlinks), end= ' ')
        li = list(links_crawled[i].outlinks_dict)
        print(li[:4], end=' ')
        print('...etc')
        print('\tINCLUDES KEY TERM? ', end=' ')
        if key_term in li:
            print('YES')
        else:
            print('NO')
        print('\tINCLUDES DICTIONARY TERM? ', end=' ')
        for a in li:
            if a in links_crawled:
                print('YES - ' + a, end=' ')
                break
        print()
    #
    #


def main():
    time_start = time.time()
    scrape_wiki()
    time_end = time.time()
    print('Time elapsed: ' + str(time_end - time_start) + ' sec')


if __name__ == '__main__':
    main()
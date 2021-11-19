import csv
from crawler import page

# See how-to.txt in data folder for more sample data
WIKI_DATA = 'data/wiki-repo-final.csv'

# pagerank algorithm will work by:
#   Going through the linksCrawled dictionary
#   For each URL (key), calculate pagerank
#   Check each page object in linksCrawled dictionary to see if that page's
#       outlinks list contains the URL of page we are trying to calculate.
#   If it does, then include it in the calculation for the pagerank
#   REMEMBER: Use the pagerank of the previous iteration (look at lecture slides for detail)


# Builds a dictionary from .csv file
def build_dict(file):
    link_dict = {}
    with open(file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, skipinitialspace=True)
        for row in csv_reader:
            # remove trailing comma from .csv
            row.remove(row[-1])
            # convert outlinks to int
            row[1] = int(row[1].replace('\'',''))

            # create empty page object
            new_page = page(0)
            if row[1] != 0:
                for i in row[2:]:
                    # add outlinks as dictionary entries with value 0
                    new_page.outlinksDict[i] = 0
                # update number of outlinks
                new_page.outlinks = row[1]
            # add page object to new dictionary
            link_dict[row[0]] = new_page
    return link_dict


def main():
    # open .csv and build dictionary
    wiki_dict = build_dict(WIKI_DATA)
    # sample output for wiki_dict: ########
    dict_keys = list(wiki_dict.keys())
    for i in range(0, 20):
        print("Topic:", end=' ')
        print(dict_keys[i], end='\nNumber of outlinks: ')
        print(wiki_dict[dict_keys[i]].outlinks, end='\nOutlinks: ')
        print(wiki_dict[dict_keys[i]].outlinksDict)
    # end sample output ##################


if __name__ == '__main__':
    main()
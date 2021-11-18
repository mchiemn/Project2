import csv
from crawler import page

# pagerank algorithm will work by:
#   Going through the linksCrawled dictionary
#   For each URL (key), calculate pagerank
#   Check each page object in linksCrawled dictionary to see if that page's outlinks list contains the URL of page we are trying to calculate.
#   If it does, then include it in the calculation for the pagerank
#   REMEMBER: Use the pagerank of the previous iteration (look at lecture slides for detail)


# Builds dictionary from .csv file
def build_dict(file):
    link_dict = {}
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar=' ', )
        new_page = page(0)
        for row in csv_reader:
            # remove trailing comma from .csv
            row.remove(row[-1])
            row[1] = int(row[1].replace('\'',''))

            new_page = page(0)
            if row[1] != 0:
                for i in row[2:]:
                    new_page.outlinksDict[i] = 0
                new_page.outlinks = row[1]
            link_dict[row[0]] = new_page
    return link_dict


def main():
    # Open .csv and build dictionary
    f = 'data/wiki-repo-filtered.csv'
    wiki_dict = build_dict(f)
    ## sample output for wiki_dict: ##
    dict_keys = list(wiki_dict.keys())
    for i in range(0,15):
        print("Topic:", end=' ')
        print(dict_keys[i], end='\nNumber of outlinks: ')
        print(wiki_dict[dict_keys[i]].outlinks, end='\nOutlinks: ')
        print(wiki_dict[dict_keys[i]].outlinksDict)
    ## end sample output ##



if __name__ == '__main__':
    main()
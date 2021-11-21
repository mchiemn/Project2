import csv
from crawler import page
import copy

# See how-to.txt in data folder for more sample data
WIKI_DATA = 'data/wiki-repo-final.csv'

# pagerank algorithm will work by:
#   Going through the linksCrawled dictionary
#   For each URL (key), calculate pagerank
#   Check each page object in linksCrawled dictionary to see if that page's
#       outlinks list contains the URL of page we are trying to calculate.
#   If it does, then include it in the calculation for the pagerank
#   REMEMBER: Use the pagerank of the previous iteration (look at lecture slides for detail)


def page_rank(dictionary, iterations):
    #this dict is used to store the values to be used in the current iteration
    temp_PR_dict = init_temp_PR_dict(dictionary)

    #key: page topic, value: list of pages that link to the key
    inlinks_dict = {}
    for k in dictionary.keys():
        inlinks_dict[k] = get_inlinks(dictionary, k)
    
    for i in range(iterations):

        #for each page in our dictionary
        for k in dictionary.keys():
            temp = 0

            #go through its inlinks
            for inlink in inlinks_dict[k]:

                #add each inlink's (PageRank/ number of outlinks)
                temp += temp_PR_dict[inlink]/dictionary[inlink].outlinks
            
            #update the page's pagerank !!in the object!! (temp_PR_dict still has old value)
            dictionary[k].pagerank = temp
        
        #now that the iteration is complete, update temp_PR_dict with PR values for the next iteration
        update_temp_PR_dict(dictionary, temp_PR_dict)
    
    #print the last iteration for now i guess
    print(temp_PR_dict)


def random_surfer_adjustments():
    pass

#returns a list of inlinks for a page
def get_inlinks(dictionary, target_page):
    inlinks_list = []
    for k in dictionary.keys():
        if target_page in dictionary[k].outlinksDict.keys():
            inlinks_list.append(k)
    return inlinks_list

#initializes a dictionary with each page and its initial pagerank (1/ number of pages)
def init_temp_PR_dict(dictionary):
    temp = {}
    init_PR = 1/len(dictionary)
    for k in dictionary.keys():
        temp[k] = init_PR
    return temp

#updates temporary dictionary with new pageranks to be used in the next iteration
def update_temp_PR_dict(dictionary, temp_dict):
    for k in dictionary.keys():
        temp_dict[k] = dictionary[k].pagerank
    return temp_dict

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

    #get_temp_PR_dict(wiki_dict)
    '''for i in range(0, 20):
        print("Topic:", end=' ')
        print(dict_keys[i], end='\nNumber of outlinks: ')
        print(wiki_dict[dict_keys[i]].outlinks, end='\nOutlinks: ')
        print(wiki_dict[dict_keys[i]].outlinksDict)'''
    # end sample output ##################


    page_rank(wiki_dict, 10)



if __name__ == '__main__':
    main()
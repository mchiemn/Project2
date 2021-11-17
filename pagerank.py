from crawler import linksCrawled

# pagerank algorithm will work by:
#   Going through the linksCrawled dictionary
#   For each URL (key), calculate pagerank
#   Check each page object in linksCrawled dictionary to see if that page's outlinks list contains the URL of page we are trying to calculate.
#   If it does, then include it in the calculation for the pagerank
#   REMEMBER: Use the pagerank of the previous iteration (look at lecture slides for detail)
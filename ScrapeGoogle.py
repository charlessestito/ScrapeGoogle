#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib
import urllib2
import urlparse
import sys
import time
import argparse
import logging

if __name__ == '__main__':
    #Parser allows reading from STDIN to enter the site address needed
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('-v', '--verbose', action='store_const', const=logging.INFO, dest='loglevel',
                        help='increase output verbosity.')
    parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG, dest='loglevel',
                        default=logging.WARNING, help='show debug output (even more than -v).')

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    #Parser has logged the argument and now assigns it to the local variable
    var = args.query

    #Initialize number to 1 to rank the search results
    number = 1

    #Using URLLIB2 Create an opener with Mozilla User-Agent
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent','Mozilla/5.0')]

    #Print out date at top of report
    date = time.strftime("%x")
    print "#Searching Google for site:%s on %s" % (var,date)

    #Iterate through the first 5 pages of Google Search results
    for start in range(0,5):

        #Create url with STDIN input site, use start value to choose page
        address = "http://www.google.com/search?q=site:"+var+"&start="+str(start*10)

	#Open the page
        page = opener.open(address)
        
	#Call upon the most beautiful of soups to make parsable html
	soup = BeautifulSoup(page,"html.parser")

	for li in soup.findAll('li',attrs={'class':'g'}):

	    #Find result titles, strip of unwanted characters and encode in UTF-8
	    for h in li.findAll('h3'):
 	        title =   h.text
		title = title.strip('\t\n\r')
		title = title.encode('utf8')

	    #Find result URLs, strip of unwanted characters and encode in UTF-8
	    for cite in li.findAll('cite'):
	        site = cite.text
		site = site.strip('\t\n\r')
		site = site.encode('utf8')	
	
	    #Print out the results to STDOUT
	    print "%d\t%s\t%s" %(number,title,site)

	    #Increment number counter to rank search results
            number += 1


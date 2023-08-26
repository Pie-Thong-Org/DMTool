# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 22:23:29 2023

@author: Tony
"""

from bs4 import BeautifulSoup as BSoup
import pandas as ps #extra data organization, pandas.read_html is apparently slightly better than json.loads for some cases
import requests #getting source code from web pages
import json #use json.loads if pandas.read_html doesn't work
import lxml #parser, reportedly faster than python's default parser: html.parser

##############################################################################

#declarations

homepageurl = "http://dnd5e.wikidot.com"
dndhomepage = requests.get("http://dnd5e.wikidot.com")
soup = BSoup(dndhomepage.text, "lxml")

links = []

hpage_navlist = ["Weapons"]
weapontable_navlist = ["Simple Weapons"]
###############################################################################

#classes

###############################################################################

#functions

def navigate_site_level(orig_url, page_navlist, *links):
    '''
    Parameters
    ----------
    orig_url 
        Type: Str
        Desc: URL of page to be searched.
    page_navlist 
        Type: List
        Desc: List of search keywords. Hyperlinks containing these strings will be returned as output.
    *links 
        Type: List
        Desc: Optional parameter to provide additional specific urls to navigate through. This list will be appended with
        search results from page_navlist.

    Returns: List of new url strings
    -------
    Searches the given url page for hyperlinks that contain given keyword strings.
    Used to navigate the current site level through hyperlinks. The url's returned depend on the keywords
    provided in the page_navlist parameter.
    
    Notes:
        -Needs testing
        -Add error handling loops and feedback messages
    '''
    
    new_urls = []
    
    if not links:
        links = []
        
    get_links = soup.find_all("a")

    for link in get_links:
        if page_navlist:
            if link.string in page_navlist:
                links.append(link)
        else:
            break
 
    for new_link in links:
        new_urls = requests.get(f"{orig_url}{links[i]['href']}")
        new_urls.append(new_link)
        print(new_link)
    
    return new_urls

def scrape_url(nav_page, *data_org, number_of_headers):
    '''
    
    Parameters
    ----------
    nav_page : TYPE
        DESCRIPTION.
    *data_org : TYPE
        DESCRIPTION.
    number_of_headers : TYPE
        DESCRIPTION.

    Returns
    -------
    data_dict : TYPE
        DESCRIPTION.

    '''
    data_list = []
    data_dict = {}
    
    if not data_org:
        data_org = "table"
    
    if not number_of_headers:
        number_of_headers = 5
        
    nav_soup = BSoup(nav_page.text, "lxml")
    print(f"URL Return: \n {nav_soup}")
    
    page_tables = nav_soup.find_all("table")

    for table in page_tables:
        cell = table.find_all("td")
        for data in cell:
            data_list.append(data.string)

    listpack = []
    counter = 0
    for i in range(number_of_headers-1,len(data_list), number_of_headers):
        
        number_iter = number_of_headers
        for j in range(number_of_headers):
            listpack.append([number_iter+1])
            number_iter -= 1
            
        data_dict[f"{counter+1}"] = listpack
        counter += 1
       
        return data_dict

def create_json(python_dict, file_to_write):
    '''

    Parameters
    ----------
    python_dict : TYPE
        DESCRIPTION.
    file_to_write : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    jsconvert = json.dumps(python_dict, indent = 1)
    
    with open(file_to_write, "w") as file:
        file.write(jsconvert)
    
    print("file written")
    
###############################################################################

get_links = soup.find_all("a")


for link in get_links:
    if link.string in hpage_navlist:
        links.append(link)

h_nav_page = requests.get(f"{homepageurl}{links[0]['href']}")

nav_soup = BSoup(h_nav_page.text, "lxml")

print(links[0]["href"])
print(f"{homepageurl}{links[0]['href']}")

print('HOMEPAGE')
print(soup.p.prettify())  
print('WEAPONS PAGE')
print(nav_soup.p.prettify()) 

search = nav_soup.find_all("table")

headerslist = []

headersdict = {}
print(type(headersdict))

for i in search:
    i = i.find_all("td")
    for j in i:
        headerslist.append(j.string)

counter = 0
for i in range(4,len(headerslist), 5):
    tuplepack = (headerslist[i-4], headerslist[i-3], headerslist[i-2], headerslist[i-1], headerslist[i])
    headersdict[f"{counter+1}"] = tuplepack
    counter += 1
   

print(headersdict)
print(counter)

jsconvert = json.dumps(headersdict, indent = 1)

with open("savefile.json", "w") as file:
    file.write(jsconvert)



















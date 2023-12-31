# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 22:23:29 2023

@author: Tony
"""
"""
Created on Mon Aug 21 22:23:29 2023

@author: Tony
"""

'''
needs specific functions:
    - weapons page, "Setting Specific Weapons" table
'''
import bs4
from bs4 import BeautifulSoup as BSoup
import pandas as ps #extra data organization, pandas.read_html is apparently slightly better than json.loads for some cases
import requests #getting source code from web pages
import json #use json.loads if pandas.read_html doesn't work
import lxml #parser, reportedly faster than python's default parser: html.parser
import time

##############################################################################

#declarations

homepage_url = "http://dnd5e.wikidot.com"
#dndhomepage = requests.get("http://dnd5e.wikidot.com")
#soup = BSoup(dndhomepage.text, "lxml")

links = []

hpage_navlist = ["Weapons"]
weaponspage_headers = ["Simple Weapons", "Martial Weapons", "Ammunition", "Setting Specific Weapons"]
weaponspage_extra_headers = ["Setting Specific Weapons"]
weaponspage_secondary_filter = ["Name", "Cost","Damage", "Weight","Properties","Simple Melee Weapons","Simple Ranged Weapons", "Martial Melee Weapons", "Martial Ranged Weapons", "Ammunition"]

id_index = 0

num_requests = 0 #request tracker
request_delay = 1 #higher number slows scraping process, increases time between requests to reduce server load. 1 or more should be safe. Not recommended to go <1 second/request

#page = requests.get(f"{homepage_url}/weapons")
#soup = BSoup(page.text, "lxml")
#print(soup.table)
###############################################################################

#classes

###############################################################################

#functions

def navigate_site_level(orig_url, page_navlist, final, *anchors):
    '''
    Parameters
    ----------
    orig_url 
        Type: Str
        Desc: URL of page to be searched.
    page_navlist 
        Type: List of str's
        Desc: List of search keywords. Hyperlinks containing these strings will be returned as output.
    final
        Type: Bool
        Desc: States whether or not this is the lowest level of navigation desired(are you at the page to be scraped?).
        A True value here will cause the function to return a list of requests.response objects. False will give a return of
        str's for new urls to be navigted through.
    *links 
        Type: List of BSoup.tag objects
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
    print("navigating...")
    print(orig_url)
    print(page_navlist)
    print("...")
    #pulls in global request tracker variable
    global num_requests
    #handle declarations and default values for optional parameters
    new_pages = [] #this will store responses from new urls
    new_urls = []  #this will store the actual link string from new urls
    
    if not anchors:
        anchors = []
    
    #get the soup text (html) for the current page. This creates a request.
    orig_page = requests.get(orig_url) 
    soup = BSoup(orig_page.text, "lxml")
    time.sleep(request_delay)#shuold time.sleep for at least one second every time a request is made, to keep server loads safe.
    num_requests += 1
    
    # searches soup for all 'a' tags(usually contain hyperlinks). This returns a list of BSoup.tag objects.
    get_anchors = soup.find_all("a")
    
    
    for anchor in get_anchors:
        if page_navlist:
            if anchor.string in page_navlist:
                anchors.append(anchor)
        else:
            break   
    print(anchors)
    print("...") 
    
    # CAUTION: Creates multiple requests to the server. This adds the 'href' attribute value(the modification of the url) to the end of the current page url, the new one created is used to navigate to that new page. Returns a response from that new url page.
    for i in enumerate(anchors):
        print(f"new url: {orig_url}{anchors[i[0]]['href']}")
        if final:
            new_page = requests.get(f"{orig_url}{anchors[i[0]]['href']}")
            new_pages.append(new_page)
            time.sleep(request_delay)
            num_requests += 1
        new_urls.append(f"{orig_url}{anchors[i[0]]['href']}")
    
    time.sleep(0.5)
    print("...")
        
    #pause to help reduce request load(not totally necessary, but adds a few seconds just to be safe)
    print("....")
    time.sleep(5)
        
    if final:
        print(f"page(s) ready for scraping: {len(new_pages)}")
        return new_pages
    else:
        print(f"new urls obtained: {new_urls}")
        return new_urls
    
def populate_dictionary(number_of_columns, data_list):
    
    if not number_of_columns:
        number_of_columns = 5
    
    data_dict = {}
    
    counter = 0
    for i in range(number_of_columns,len(data_list)+1, number_of_columns):
        
        number_iter = i-number_of_columns
        listpack = []
        for j in range(number_of_columns):
            listpack.append(data_list[number_iter+j])
                  
        data_dict[f"{counter+1}"] = listpack
        counter += 1
      
    return data_dict

def scrape_tables(web_page, header_flags, extra_header_flags, secondary_filters, *data_format):
    '''
    
    Parameters
    ----------
    nav_page : TYPE
        DESCRIPTION.
    header_flags:
        Type: List of Str's
        Desc: 
    extra_header_flags:
        Type: List of Str's
        Desc: These are for headers with another sub-header before the table. These will get 'drilled' an extra time. kinda like ur mom lol
    number_of_columns : TYPE
        DESCRIPTION.
    *data_format :
        Type: Str
        Desc: "table", "p"...

    -eventually expand this to handle different data formats by using the relevant arguments?
    
    Returns
    -------
    data_dict : TYPE
        DESCRIPTION.

    '''
    global num_requests
    global request_delay
    global id_index
    
    data_list = []
    data_dict = {}
    
    if not data_format:
        data_format = "table"
         
    soup = BSoup(web_page.text, "lxml")
    #print(f"URL Return: \n {soup}")
    
    
    #filters tables to scrape by their headers. This will keep it from grabbing extra info from the page that's not wanted.
    headers = soup.find_all("h1")
    
    column_counter = 0
    counter = 0
    for h in headers:
        if h.text in header_flags:
            print(f"########################################################## \n {h.text} \n")
            c = h.next_sibling.next_sibling #find a way to be more adaptive to the web page? Currently this navigation works for the weapons table on dndwiki due to the layout, though unknown if it will work elsewhere.
            
            for i in c:
                #print(i)
                
                for j in i:
                    if type(j) == bs4.element.Tag: #skips over siblings that are empty spaces so that columsn can be counted correctly
                        if j.string not in secondary_filters and j.string[0] not "*": #skips over any string specified in the secondary_filters list. This should be used for secondary headers that aren't part of the actua l data.
                            data_list.append(j.string)
                            column_counter += 1
                           
                if column_counter:
                    num_columns = column_counter
                    #print(f"columns: {num_columns}")
               
                column_counter = 0
                
            data_dict = populate_dictionary(num_columns, data_list)
            #######temp write to .json file. For testing only. Will be using save_to_json in the future
            with open(f"savefile{id_index}.json", "a") as file:
                data_dict = {"_id": id_index, h.text : data_dict}
                jsconvert = json.dumps(data_dict, indent = 1)
                file.write(jsconvert)
                id_index += 1
            ########   
            data_list = []   
            #print(data_dict)
            
            
    '''            
    tables = soup.find_all("table")
    
    for table in tables:
        cell = table.find_all("td")
        for data in cell:
            data_list.append(data.string)
    '''


def save_to_json(python_dict, file_to_write, read_type):
    '''

    Parameters
    ----------
    python_dict : TYPE
        DESCRIPTION.
    file_to_write : TYPE
        DESCRIPTION.
    read_type: 
        Type: Str - "w", "a"
        Desc: Write over or append to .json 

    Returns
    -------
    None.

    '''
    jsconvert = json.dumps(python_dict, indent = 1)
    
    with open(file_to_write, read_type) as file:
        file.write(jsconvert)
    
    print("file written")
    
###############################################################################

'''get_links = soup.find_all("a")


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
'''

#new_pages = navigate_site_level(homepage_url, hpage_navlist, final = True)
#print(new_pages)
page = requests.get("http://dnd5e.wikidot.com/weapons") 
num_requests += 1
data = scrape_tables(page,header_flags = weaponspage_headers, extra_header_flags = weaponspage_extra_headers, secondary_filters = weaponspage_secondary_filter)

file_data = json.dumps(data, indent = 1)
#print(file_data) 


print(f"Finished. requests made: {num_requests}")



















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

file = open("savefile.json", "w")

links = []
hpage_navlist = ["Weapons"]
weapontable_navlist = ["Simple Weapons"]
###############################################################################

#classes

###############################################################################

#functions

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

file.write(jsconvert)



















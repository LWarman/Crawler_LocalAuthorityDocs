# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 18:44:33 2019

@author: lucyc
"""

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import json

valid = 0
validSite = []
request = ()
LAsjson = 'C:\\Users\\cslw1\\Desktop\\AllCouncils.json'
floodKeys = 'C:\\Users\\cslw1\\Desktop\\FloodSearch.json'
cleanListjson = 'C:\\Users\\cslw1\\Desktop\\LinkCleaner.json'

allSiteLinksTest = 'C:\\Users\\cslw1\\Desktop\\CouncilPages\\allSiteLinksTest'
allFloodDocsTest = 'C:\\Users\\cslw1\\Desktop\\CouncilPages\\allFloodDocsTest'

number = 0

#------------------------------------------------------------------------------
def isValid(site):
    request = requests.get(site)
    if request.status_code < 400:
        valid = 1
    else:
        valid = 0

    return valid
#------------------------------------------------------------------------------
def readPage(validPage):
    html = urlopen(validPage)
    soup = BeautifulSoup(html, 'lxml')
    title = soup.title
    
    return {'title': title, 'text' : soup}
#------------------------------------------------------------------------------    PAGES
def searchPage(pageText, searchType, homePage, rootPage, pageList, internalPageCheck):
    pageLinks = []
    setList = []

    linksInPage = pageText.find_all('a')
    if searchType == 'links':
        for i in linksInPage:            
            if "pdf" in i:
                continue
            if i.get('href') not in pageList:
                pageLinks.append(i.get('href'))
            


#------------------------------------------------------------------------------    DOCS              
                
    if searchType == 'docs':
        pageLinks = []
        setList = []
        for j in docList:
            for i in linksInPage:
                if j in i:
                    print(j)
                    print(i)
                    print(i.get('href'))
                    if "pdf" in i.get('href'):
                       if i.get('href') not in pageList:
                        pageLinks.append(i.get('href'))
                        print(i)
                        set(pageLinks)
                    else:
                        continue

#------------------------------------------------------------------------------    RETURN  
    else:
        pass

    pageLinks = clean(pageLinks, homePage, rootPage, pageList, internalPageCheck)
    for x in pageLinks:
        if x in pageList:
            continue
        else:
            setList.append(x)
            set(setList)
    return setList


#------------------------------------------------------------------------------
def clean(Links, homePage, rootPage, pageList, internalPageCheck):
    cleanLinks = []
    linksUpdate = []
    cleanedLinks = []
#--------- remove links to social media/blogs etc
    for y in Links:
        if y in pageList:
            continue
        if y is None:
            continue
        if 'infonet' in y:
            continue
        if 'pdf' in y:
            continue
        if 'mailto' in y:
            continue
        for i in cleanList:
            if i in y:
                continue
#        if 'mailto' in l:
#            continue
        else:
            linksUpdate.append(y)
#            print(len(linksUpdate))
#--------- add homepage to relative links
    for x, item in enumerate(linksUpdate):
        if len(item) == 0:
            continue
        if item[0] == "/":
#            print(item)
            linksUpdate[x] = rootPage + item
            cleanLinks.append(linksUpdate[x])
#        if homePage not in item:
#            continue
        else:
            cleanLinks.append(linksUpdate[x])
#--------- only return pages which are on a .gov website
    for y in cleanLinks:
        if '.gov.' not in y:
            continue
        if internalPageCheck not in y:
            continue
        else:
            cleanedLinks.append(y)

    set(cleanedLinks)

    return cleanedLinks
#------------------------------------------------------------------------------
def findPages(page, pageList, searchFor, homePage, rootPage, internalPageCheck):     

    siteText = readPage(page)
    pageText = siteText['text']
#        siteTitle = siteText['title']
#        pageList = []
#    print(type(pageList))

    pageList = pageList + searchPage(pageText, searchFor, homePage, rootPage, pageList, internalPageCheck)
    return pageList
#------------------------------------------------------------------------------

with open(LAsjson, 'r') as f:
    siteList = json.load(f)

with open(cleanListjson, 'r') as j:
    cleanList = json.load(j)

with open(floodKeys, 'r') as f:
    docList = json.load(f)

for a in siteList:
#    number = number + 1
    valid = isValid(a)
    if valid == 1:
        validSite.append(a)
    else:
        pass

    for b in validSite:
        firststop = b.find('.')
        secondpoint = b.find('.', (firststop+1), len(a))
        firstpoint = firststop + 1
        homePage = b[firstpoint:secondpoint]
        rootPage = b[:-1]
        internalPageCheck = rootPage[4:]
        searchFor = 'links'
        linkList = []
        floodList = []
        linkList = linkList + [b]
        linkList = findPages(b, linkList, searchFor, homePage, rootPage, internalPageCheck)

        for c in linkList:
            linkList = findPages(c, linkList, searchFor, homePage, rootPage, internalPageCheck)
            
        fileNamePages = allSiteLinksTest + '_' + homePage + '.txt'
        with open (fileNamePages, 'w') as a:
            a.write('\n'.join(line for line in linkList))

        for d in linkList:
            searchFor = 'docs'
            floodList = findPages(d, linkList, searchFor, homePage, rootPage, internalPageCheck)
        fileNameDocs = allFloodDocsTest + '_' + homePage + '.txt'

        with open (fileNameDocs, 'w') as a:
                a.write('\n'.join(line for line in floodList))        

        linkList = set(linkList)
        floodList = set(floodList)
    
        print(len(linkList))
        print(len(floodList)) 
#        floodList = set(floodList)
   
             
    






    
#    for x in pageLinks:
#        searchFor = 'docs'
#        siteText = readPage(i)
#        pageText = siteText['text']
#        pageLinks = searchPage(pageText, searchFor)


#    searchFor = 'docs'
#    pageText = readPage(i)
#    pageLinks = searchPage(pageText, searchFor)
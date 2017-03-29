#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 11:01:45 2017
@author: sabyasachi

FPL league table scrapping
"""

from bs4 import BeautifulSoup
import requests
import csv


#make the soup
url_fpl = 'https://www.premierleague.com/tables'
page = requests.get(url_fpl)
contents = page.content
soup = BeautifulSoup(contents, 'lxml')

soup.prettify


#The table details
table = soup.find_all("tbody", { "class" : "tableBodyContainer" })[:1]
#Get team names
teams = soup.find_all("span",{"class":"long"})[:20]
#position
position = soup.find_all("span",{"class","value"})[:20]
#Points data fetch
points = soup.find_all("td",{"class":"points"})[:20]
#Headers fetch
headers = soup.find_all("div",{"class":"thFull"})[0:]

#Initialize data
teamNames = []
teamPos = []
teamPts = []
indexes = []
data = []

#Extract the team names
for row in teams:
    teamNames.append(row.get_text())
#Extract the postion
for row in position:
    teamPos.append(row.get_text())
#Extract the points
for row in points:
    teamPts.append(row.get_text())   

#getting the indices
def indices(l, val):
    """always returns a list containing the indices of val in l
    """
    retval = []
    last = 0
    for item in val[last:]:
        i = l[last:].index(item)
        retval.append(last + i)
        last += i + 1   
    return retval   

#Used for writing the CSV file
def writeCSV(data_list):
    with open('team_details.csv', 'w') as data_file:
        csv_writer = csv.writer(data_file)
        for data in data_list:
            csv_writer.writerow([s.encode('utf-8') for s in data])  # write csv values in unicode 

#append the headers
data.append(['Position','Teams','Played','Won','Drawn','Lost', 'Goals For', 'Goals Against','Goal Diff.','Points'])
index = 0   
a = 0 
#Extract the table details    Played Won Drawn Lost GF	GA
for row in table:
    nexttime = 0
    cells = soup.find_all("td")
    scope_data = soup.find_all("td",{"scope":"row"})
    #Get all indexes
    indexes = indices(cells,scope_data)
    for a in indexes:  
            try:
                pld = cells[a+1].get_text()
                won = cells[a+2].get_text()
                dwn = cells[a+3].get_text()
                lost = cells[a+4].get_text()
                gf = cells[a+5].get_text()
                ga = cells[a+6].get_text()
                gd = cells[a+7].get_text()
                gd = gd.replace('\n', ' ').replace('\r', '')
                data.append([teamPos[index],teamNames[index],pld,won,dwn,lost,gf,ga,gd,teamPts[index]])
                index+=1
            except:
                pass
 
#Now write this data in a csv    
writeCSV(data)




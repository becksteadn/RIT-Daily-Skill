##
#Python script to parse data from the RIT Daily News and Events Webpage
#
#Author: Nathaniel Beckstead becksteadn@gmail.com
#
#Last update: 4/24/2017
##
#Notes: 'eleven columns clearfix' for main body div
import requests
from bs4 import BeautifulSoup

URL_DAILY = "https://www.rit.edu/news/nandedaily.php"
PAGE_DAILY = "page_daily.txt"


def getPage(url):
    return requests.get(url).text

def getDiv(content, header):
    soup = BeautifulSoup(content, "lxml")
    right_col = soup.find_all('div', {'class':'four columns omega right_side'})[0]
    head = 0
    for tagnum in range(len(right_col.contents)):
        child = right_col.contents[tagnum]
        if(child.string == header):
            head = tagnum + 1
            break
    return right_col.contents[head]

def getNews():
    return 0

def getEvents(content):
    events = list()
    events_div = getDiv(content, "Upcoming Events")
    for n in range(len(events_div.contents)):
        tag = events_div.contents[n]
        if(tag.name == "strong"):
            title = tag.string
            
            #Advance to next tag
            n += 1
            tag = events_div.contents[n]
            
            desc = tag.string
            events.append(title.upper() + desc)
    return events

def splitEvent(event):
    return

def getSports(content):
    sports = list()
    sports_div = getDiv(content, "Scoreboard")    
    for n in range(len(sports_div.contents)):
        tag = sports_div.contents[n]
        if(tag.name == "strong"):
            team = tag.string

            n += 1
            tag = sports_div.contents[n]

            score = tag.string
            
            sports.append(team + score)
    return sports

if __name__ == "__main__":
    webText = getPage(URL_DAILY)
    events = getEvents(webText)
    for event in events:
        print(event)
    sports = getSports(webText)
    for sport in sports:
        print(sport)

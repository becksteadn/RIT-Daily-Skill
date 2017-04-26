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
from datetime import date, datetime

URL_DAILY = "https://www.rit.edu/news/nandedaily.php"
PAGE_DAILY = "page_daily.txt"

def update():
    real_today = date.today().strftime("%B %d, %Y")
    page_today = ""
    with open(PAGE_DAILY, "r") as f:
        page_today = f.readline().strip()
    
    return False if real_today == page_today else True        

def getPage(url):
    with open(PAGE_DAILY, "r+") as f:
        real_today = getRealDate() 
        text = f.readlines()
        try:
            textdate = text.pop()
        except IndexError:
            textdate = ""
        if(textdate != real_today):
            print("Getting page...")
            newtext = requests.get(url).text
            f.seek(0)
            f.write(real_today + "\n")
            f.write(newtext)
            f.truncate()
            return newtext
        else: #same day, return same page
            return text.join()

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

def getRealDate():
    return date.today().strftime("%B %d, %Y")

#Deprecated
def getDate(content):
  # # soup = BeautifulSoup(content, "lxml")
    todaysdate = soup.find_all('div', {'class':'eleven columns alpha'})[0].contents[1].contents[1].string
    print(todaysdate)

def getWeather(content):
    return

def getNews(content):
    return

def getEvents(content):
    events = list()
    events_div = getDiv(content, "Upcoming Events")
    for n in range(len(events_div.contents)):
        tag = events_div.contents[n]
        if(tag.name == "strong"):
#            hier = str(tag.name) #####

            title = tag.string
             
            #Advance to next tag
            n += 1
            tag = events_div.contents[n]           

#            hier += " " + str(tag.name) #####

            desc = tag.string

            desc2 = ""
            if(desc.name == "em"):
                n += 1
                tag = events_div.contents[n]

#                hier += " " + str(tag.name) #####

                desc2 = tag.string

#            print(hier)
            events.append(title.upper() + desc + desc2)
    return events

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

def alexaGet():
    if(update()):
        print("Updating, " + getRealDate())
        webText = getPage(URL_DAILY)

        events = getEvents(webText)
        with open("events.txt", "w") as f:
            for event in events:
                f.write((event + "\n").encode("utf-8"))

        sports = getSports(webText)
        with open("sports.txt", "w") as f:
            for sport in sports:
                f.write((sport + "\n").encode("utf-8"))

    events = ""
    with open("events.txt", "r") as f:
        events = "".join(f.readlines())

    sports = ""
    with open("sports.txt", "r") as f:
        sports = "".join(f.readlines())

    return (events, sports)

def printEvents():
    return alexaGet()[0]

def printSports():
    return alexaGet()[1]

if __name__ == "__main__":
    daily = alexaGet()
    HEAD = "-" * 10
    print(HEAD + " Events " + HEAD)
    print(daily[0])
    print(HEAD + " Sports " + HEAD)
    print(daily[1])




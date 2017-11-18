from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

laundry_url = "http://m.laundryview.com"

tags = ["est. time remaining","extended cycle running for",\
        "cycle ended","out of service","unknown",\
        "cycle has ended - door still closed","available"]

def heat_soup(url):
    """ grabs the soup from the url """
    campus_html = urlopen(url).read()
    return BeautifulSoup(campus_html,"html.parser")

def clean(string):
    """ cleans and returns the string given """
    return string.replace('\t','').replace('\n','').replace('  ','')

def collect_campus():
    """ returns a dictionary of campus locations {url:name}"""
    soup = BeautifulSoup(urlopen(laundry_url).read(),"html.parser")
    campus_locations = {}

    for link in soup.find_all('a'):
        if "lvs" in link['href']:
            location_name = clean(link.string)
            location_link = link['href']
            campus_locations[location_link] = location_name

    return campus_locations

def collect_buildings(campus_url):
    """ returns a dictionary of buildings {url:name}"""
    buildings = {}
    campus_soup = heat_soup(laundry_url+"/"+campus_url)

    for item in campus_soup.find_all('li'):
        a_tags = item.find_all('a')
        # remove the last two values [home,options]
        for a in a_tags:
            if "Home" in a.string or "Options" in a.string:
                continue
            buildings[a['href']] = clean(a.string)

    return buildings

def collect_room(room_url):
    """ returns a list of stats for the room """
    room  = {}
    room_soup = heat_soup("http://classic.laundryview.com/"+room_url)

    stats = room_soup.find('div',{'class':'monitor-total'})
    dryer_available = stats.contents[2].split(" ")[1:4]
    washer_available = stats.contents[4].split(" ")[1:4]

    dryers = room_soup.find('td',{'align':'left','class':'bgwhite'})
    dryers = [clean(stat.string) for stat in dryers.find_all('span',{'class':'stat'})]

    washers = room_soup.find('td',{'align':'right','class':'bgwhite'})
    washers = [clean(stat.string) for stat in washers.find_all('span',{'class':'stat'})]

    room['dryer'] = [dryer_available, dryers]
    room['washer'] = [washer_available,washers]

    return room

def collect_heatmap(room_url):
    """ returns a dictionary of the heatmap of use """
    heatmap = []
    heatmap_soup = heat_soup("http://admin.laundryview.com/usage/"+room_url.split("php")[1])

    heatmap_table = [i.contents for i in heatmap_soup.findAll('table')[2].findAll('tr')]

    for num in range(0, len(heatmap_table), 6):
        hm = heatmap_table[num]
        day = hm[1].string

        hours = []
        for i in range(5,21,4):
            hour_block = [usage['class'] for usage in hm[i].contents[1].find_all('td')]
            for hour in hour_block:
                #convert the tags to a measureable scale before appending
                if 'bgcream' in hour:
                    hour = 0
                elif 'bgyellow' in hour:
                    hour = 1
                elif 'bgred' in hour:
                    hour = 2
                else:
                    hour = None
                hours.append(hour)
        heatmap.append((day,hours))
    return heatmap

if __name__ == "__main__":
    campus = collect_campus()
    buildings = {}
    room = {}

    # print the all the buildings in the first campus
    for url, name in campus.items():
        print(name)
        buildings = collect_buildings(url)
        print(buildings,"\n")
        break

    #print the floors in the fist building in the list
    for url, name in buildings.items():
        print(name)
        room = collect_room(url)
        print('usage: 6am -> 5am', collect_heatmap(url), "\n")
        break

    print(room['dryer'])
    print(room['washer'])

from bs4 import BeautifulSoup
from urllib.request import urlopen
laundry_url = "http://m.laundryview.com"

def collect_campus():
    """ returns a dictionary of campus locations """
    soup = BeautifulSoup(urlopen(laundry_url).read(),"html.parser")
    campus_locations = {}
    for link in soup.find_all('a'):
        if "lvs" in link['href']:
            location_name = link.string.replace("  ", "").replace("\n","")
            location_link = link['href']
            campus_locations[location_name] = location_link
    return campus_locations

def collect_buildings(campus_url):
    """ returns a dictionary of buildings """
    buildings = {}
    campus_html = urlopen(laundry_url+"/"+campus_url).read()
    campus_soup = BeautifulSoup(campus_html,"html.parser")
    for item in campus_soup.find_all('li'):
        a_tags = item.find_all('a')
        # remove the last two values [home,options]
        for a in a_tags:
            if "Home" in a.string or "Options" in a.string:
                continue
            buildings[a['href']] = a.string.replace("  ","")
    return buildings

def clean(string):
    return string.replace('\t','').replace('\n','').replace('  ','')

def collect_room(room_url):
    room = {}
    room_html = urlopen("http://classic.laundryview.com/"+room_url).read()
    room_soup = BeautifulSoup(room_html,"html.parser")

    stats = room_soup.find('div',{'class':'monitor-total'})
    dryer_available = stats.contents[2].split(" ")[1:4]
    washer_available = stats.contents[4].split(" ")[1:4]

    dryers = room_soup.find('td',{'align':'left','class':'bgwhite'})
    dryers = [clean(stat.string) for stat in dryers.find_all('span',{'class':'stat'})]

    washers = room_soup.find('td',{'align':'right','class':'bgwhite'})
    washers = [clean(stat.string) for stat in washers.find_all('span',{'class':'stat'})]

""" a script to collect unique tags for machines on campus """
from laundry_view import *
import datetime, notify2

tags = []

campus = collect_campus()
buildings = {}
room = {}

start_time = datetime.datetime.now()
count = 0

# set up the notifier
notify2.init("Tag Collection Notifier")
n = notify2.Notification("Tag Collection Progress")
n.set_urgency(notify2.URGENCY_NORMAL)
n.set_timeout(3000)

# print the all the buildings in the first campus
for name, url in campus.items():
    count = count + 1
    print(name)
    buildings = collect_buildings(url)
    print(buildings,"\n")

    #print the floors in the fist building in the list
    for url, name in buildings.items():
        print(name)
        room = collect_room(url)
        print(room['dryer'])
        print(room['washer'])

        # to save logic space, append and convert to set
        for tag1, tag2 in zip(room['dryer'][1],room['dryer'][1]):
            tags.append(tag1)
            tags.append(tag2)
            tags = [i for i in set(tags)]

#notify the user

    n.update("Tag Collection", str(count) + " out of " + str(len(campus)) + " inspected..")
    n.show()
    print("[",count,"out of",len(campus),"] Time Elapsed:",datetime.datetime.now() - start_time)

with open('tag_file','w') as f:
    for tag in tags:
        f.write(tag+"\n")

n.update("Tag Collection", "tag collection complete")
n.set_timeout(5000)
n.show()

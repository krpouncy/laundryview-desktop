""" this will be the window manager """
import laundry_view as lv

#personal stored information of user
my_campus = ""

def getting_started():
    print("What Campus are You At?")
    campuses = lv.collect_campus()
    count = 0
    for url, campus in campuses.items():
        name = campus.split("- ")[1:]
        clean_name = str(count) + " "
        for part_name in name:
            clean_name += part_name
        print(clean_name)
        count = count + 1
    print()

    while True:
        try:
            my_campus = [url for url,name in campuses.items()][int(input("(int)-> "))]
            break
        except:
            print("invalid response")
    print(my_campus,"\n Collecting Buildings...")

    print("Where do you reside?")
    buildings = lv.collect_buildings(my_campus)
    count = 0
    for url, building in buildings.items():
        print(count, building)
        count = count + 1
    print()
    while True:
        try:
            my_room = [url for url,name in buildings.items()][int(input("(int)-> "))]
            break
        except:
            print("invalid response")
    print(my_room)
    print()
    print("Here what's up at the moment")
    for key, value in lv.collect_room(my_room).items():
        print(key, value)

    print("\nHere's a heatmap of when the room is the busiest")
    for day, hours in lv.collect_heatmap(my_room).items():
        time = ["6am","7am","8am","9am","10am","11am","12pm","1pm","2pm","3pm","4pm","5pm",\
        "6pm","7pm","8pm","9pm","10pm","11pm","12am","1am","2am","3am","4am","5am"]

        busy_times = []
        sort_of_busy_times = []
        best_times = []

        for i in range(len(hours)):
            if hours[i] == 2:
                busy_times.append(time[i])
            elif hours[i] == 1:
                sort_of_busy_times.append(time[i])
            else:
                best_times.append(time[i])

        print("DAY:", day)
        print("busy_times",busy_times)
        print("sort_of_busy_times",sort_of_busy_times)
        print("best_times", best_times,"\n")

if __name__ == "__main__":
    getting_started()

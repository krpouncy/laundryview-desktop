""" this will be the window manager """
import laundry_view as lv
import tkinter as tk
from tkinter import ttk

class LaundryForm(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent.topFrame)
        self.parent = parent

        # some variables needed for the methods
        self.buildings = {}
        self.names = {}
        self.rooms = {}

        self.campus_label = ttk.Label(self,text="Campus", font="Calibri 11", padding='5 0 2 0')
        self.campus_label.grid(row=0,column=0,sticky='n')

        self.room_label = ttk.Label(self,text="Room", font="Calibri 11", padding='10 0 2 0')
        self.room_label.grid(row=0,column=3,sticky='n')

        # generate a clean list of campus names
        campuses = lv.collect_campus()
        for url, campus in campuses.items():
            #clean the name by removing the school's name [SCHOOL - BUILDING - NAME]
            name = campus.split("- ")[1:]
            clean_name = ''
            for part_name in name:
                clean_name += part_name
                self.names[url] = clean_name

        # create the comboboxes
        self.combo_campus = ttk.Combobox(self, values=sorted([name for _, name in self.names.items()]))
        self.combo_campus.configure(width=35)
        self.combo_campus.grid(row=0,column=1, sticky='e')
        self.combo_campus.bind('<<ComboboxSelected>>', self.submit_campus)

        self.combo_room = ttk.Combobox(self)
        self.combo_room.configure(width=35)
        self.combo_room.grid(row=0,column=4, sticky='e')
        self.combo_room.bind('<<ComboboxSelected>>', self.submit_room)

    """ note: should make it so if the value is the same don't run this method"""
    def submit_campus(self,*args):
        """ this method sets the vales for the combobox room """
        for url, clean_name in self.names.items():
            if self.combo_campus.get() == clean_name:
                self.buildings = lv.collect_buildings(url)
                self.combo_room['values'] = sorted([building for url, building in self.buildings.items()])

    def submit_room(self,*args):
        """ this will collect the laundry rooms"""
        for url, name in self.buildings.items():
            if self.combo_room.get() == name:
                self.rooms = lv.collect_room(url)
                # create the grid
                hs = self.parent.hostspot_module
                if hs:
                    hs.frm.grid_forget()
                    hs.destroy()
                hs = HotSpot(self.parent.bottomFrame,url)
                hs.pack(expand=True)

class HotSpot(ttk.Frame):
    def __init__(self, parent, url=""):
        ttk.Frame.__init__(self, parent)

        self['style'] = 'My.TFrame'
        self['padding'] = '2 2 10 10'
        self['relief'] = 'groove'

        self.url = url

        # check to see if a url is entered and valid
        if url != "":
            try:
                heatmap_list = lv.collect_heatmap(url)
                if len(heatmap_list) != 7:
                    pass
            except:
                pass
        else:
            pass

        days = ["Sun","Mon","Tues","Wed","Thu","Fri","Sat"]
        for i, day in zip(range(len(days)),days):
            ttk.Label(self,text=day,font="Calibri 11",background="#333745", foreground="white").grid(column=0,row=i+1,sticky="nse")

        time = [" 6a"," 7a"," 8a"," 9a","10a","11a","12p"," 1p"," 2p"," 3p"," 4p"," 5p",\
        " 6p"," 7p"," 8p"," 9p","10p","11p","12a"," 1a"," 2a"," 3a"," 4a"," 5a"]
        for i, hour in zip(range(len(time)),time):
            ttk.Label(self,text=hour,font="Calibri 11",width=3, background="#333745", foreground="white").grid(column=i+1,row=0)

        heat_grid = ttk.Frame(self)
        heat_grid.grid(row=1,column=1,columnspan=24,rowspan=7, sticky="nsew")

        row = 0
        for _, hours in heatmap_list:
            column = 0
            size = 32
            # create the canvas for the each day
            day_canvas = tk.Canvas(heat_grid,width=24*size,height=size,highlightthickness=0,bd=0)
            # day_canvas.grid(column = 1, row = row, sticky="nsew")
            day_canvas.pack()
            # draw the block of usage for each hour
            for usage in hours:
                if usage == 2:
                    fill = "#FF5959"
                elif usage == 1:
                    fill = "#ECC30B"
                else:
                    fill = "#84BCDA"
                day_canvas.create_rectangle(column*size, 0,(column*size)+size,(row*size)+size,fill=fill,outline="#222222")
                column += 1
            row += 1

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("LaundryView Desktop")
        self.parent.geometry("1020x500")

        # set the weights for the parent
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)

        # Time to start working on this Frame and not the Parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create the style for the frames
        self.topFrame = ttk.Frame(self, padding='5 5 5 3')
        self.topFrame.grid(row=0, column=0, sticky='nsew')

        # set the background of bottom frame
        s = ttk.Style()
        s.configure('My.TFrame',background="#333745")
        self['style'] = 'My.TFrame'

        self.bottomFrame = ttk.Frame(self, relief="sunken", style='My.TFrame')
        self.bottomFrame.grid(row=1, column=0, sticky='nsew')

        self.laundry_form = LaundryForm(self) #this is self to access the vars in self
        self.laundry_form.grid(row=0, column=0, sticky='nsew')

        self.hostspot_module = None
        # self.testLabel = ttk.Label(self.bottomFrame, text="Nothing Entered Yet")
        # self.testLabel.pack(expand=True)

if __name__ == "__main__":
    # start the Took Command Language / Tkinter Interpretor
    root = tk.Tk()
    # prevent the window from being resizable
    root.resizable(width=False, height=False)
    # draw the MainApplication
    MainApplication(root).grid(row=0, column=0, sticky='nsew')
    # start the main loop
    root.mainloop()

#
# # create the window
# window = Tk()
# window.title("LaundryView-Desktop")
# #window.geometry("480x240")
# mainframe = ttk.Frame(window)
# mainframe.grid(column=0,row=0, sticky=(N,W,E,S))

#

# window.mainloop()
# # print()
# # print("Here what's up at the moment")
# # for key, value in lv.collect_room(my_room).items():
# #     print(key, value)
# #
# # print("\nHere's a heatmap of when the room is the busiest")
# # for day, hours in lv.collect_heatmap(my_room).items():
    # time = ["6am","7am","8am","9am","10am","11am","12pm","1pm","2pm","3pm","4pm","5pm",\
    # "6pm","7pm","8pm","9pm","10pm","11pm","12am","1am","2am","3am","4am","5am"]
# #
# #     busy_times = []
# #     sort_of_busy_times = []
# #     best_times = []
# #
# #     for i in range(len(hours)):
# #         if hours[i] == 2:
# #             busy_times.append(time[i])
# #         elif hours[i] == 1:
# #             sort_of_busy_times.append(time[i])
# #         else:
# #             best_times.append(time[i])
# #
# #     print("DAY:", day)
# #     print("busy_times",busy_times)
# #     print("sort_of_busy_times",sort_of_busy_times)
# #     print("best_times", best_times,"\n")
# #
# # my_campus = []
# # try:
# #     config = open('config').read().split("\n")
# #     my_campus = config[0]
# #     #open_room()
# # except:
# #     getting_started()

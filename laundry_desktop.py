""" this will be the window manager """
import laundry_view as lv
import tkinter as tk
from tkinter import ttk

class LaundryForm(ttk.Frame):
    def __init__(self, parent, action_taken):
        ttk.Frame.__init__(self, parent.topFrame)
        self.parent = parent

        # some variables needed for the methods
        self.buildings = {}
        self.names = {}
        self.url = ""
        self.rooms = tk.StringVar()
        self.rooms.trace('w', lambda *args: action_taken())
        self.stats = {}
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
                self.url = url
                self.stats = lv.collect_room(url)
                self.rooms.set(self.stats)


class HotSpot(ttk.Frame):
    def __init__(self, parent, url=""):
        ttk.Frame.__init__(self, parent)

        self['style'] = 'My.TFrame'
        self['padding'] = '2 2 10 10'
        self['relief'] = 'ridge'

        self.url = url

        # check to see if a url is entered and valid
        heatmap_list = []
        if url != "":
            heatmap_list = lv.collect_heatmap(url)


        days = ["Sun","Mon","Tues","Wed","Thu","Fri","Sat"]
        for i, day in zip(range(len(days)),days):
            ttk.Label(self,text=day,font="Calibri 11",background="#333745", foreground="white").grid(column=0,row=i+1,sticky="nse")

        time = [" 6a"," 7a"," 8a"," 9a","10a","11a","12p"," 1p"," 2p"," 3p"," 4p"," 5p",\
        " 6p"," 7p"," 8p"," 9p","10p","11p","12a"," 1a"," 2a"," 3a"," 4a"," 5a"]
        for i, hour in zip(range(len(time)),time):
            ttk.Label(self,text=hour,font="Calibri 11",width=3, background="#333745", foreground="white").grid(column=i+1,row=0)

        heat_grid = ttk.Frame(self)
        heat_grid.grid(row=1,column=1,columnspan=24,rowspan=7, sticky="nsew")

        for i in range(1,25):
            self.grid_columnconfigure(i, weight=1)
        for i in range(1,7):
            self.grid_rowconfigure(i,weight=1)

        heat_grid['style'] = 'My.TFrame'

        row = 0
        for _, hours in heatmap_list:
            column = 0
            size = 25
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

class MachineRoom(ttk.Frame):
    def __init__(self, parent, rooms):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        # self.configure(height=200, width= 550)
        # self.grid_propagate(0)
        s = ttk.Style()
        # s.configure('MachineRoom.TFrame', background='red')
        self['style'] = 'My.TFrame'
        self['padding'] = "5"
        # self['relief'] = 'groove'
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)

        if not rooms:
            return

        dryer_num, washer_num, dryers, washers = [], [], [], []
        dryers = rooms['dryer']
        washers = rooms['washer']
        try:
            dryer_num = [int(dryers[0][0]),int(dryers[0][2])]
            washer_num = [int(washers[0][0]),int(washers[0][2])]
        except:
            pass

        for stat in dryers[1]:
            print(stat)

        # create the labels for the different sections
        ttk.Label(self,text="Dryers", font="Calibri 9",background="#333745", \
        foreground="white").grid(column=0,row=0, sticky='w')
        ttk.Label(self,text="Washers", font="Calibri 9",background="#333745", \
        foreground="white").grid(column=0,row=2, sticky='w')

        for i in range(dryer_num[1]):
            Machine(self, dryers[1][i]).grid(column=i, row=1, padx=5,pady=5)
        for i in range(washer_num[1]):
            Machine(self, washers[1][i]).grid(column=i, row=3,padx=5,pady=5)
        print(dryer_num, washer_num)

class Machine(ttk.Frame):
    def __init__(self, parent,stat):
        ttk.Frame.__init__(self, parent)
        s = ttk.Style()
        self['relief'] = 'groove'
        self.bind("<Enter>", lambda e: print(stat))
        s.configure('Running.TFrame',background="#FF5959")
        s.configure('Free.TFrame',background="#6BFFC3")
        s.configure('Dead.TFrame',background="grey")
        self.grid_propagate(0)
        self.configure(height=35, width=35)
        if "available" in stat or ("ended" in stat and "extended" not in stat):
            self['style'] = 'Free.TFrame'
        elif "est. time remaining" in stat or "extended" in stat:
            self['style'] = 'Running.TFrame'
            ttk.Label(self,text=stat[19:], font="Calibri 9", \
            foreground="black").grid(sticky='nsew')
        elif "out of service" in stat:
            self['style'] = 'Dead.TFrame'

class Notes(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.configure(height=200,width=150)

class MainApplication(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("LaundryView Desktop")
        self.parent.geometry("800x500")

        self.room_url = ""
        self.stats = {}
        # set the weights for the parent
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(0, weight=1)

        # Time to start working on this Frame and not the Parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # create the style for the frames
        self.topFrame = ttk.Frame(self, padding='5 10 5 3')
        self.topFrame.grid(row=0, column=0, sticky='nsew')
        self.topFrame.grid_propagate(0)
        self.topFrame.configure(height = 40)

        # set the background of bottom frame
        s = ttk.Style()
        s.configure('My.TFrame',background="#333745")
        self['style'] = 'My.TFrame'

        self.bottomFrame = ttk.Frame(self, style='My.TFrame')
        self.bottomFrame.grid(row=1, column=0, sticky='nsew')
        self.bottomFrame['padding'] = 30
        self.bottomFrame.grid_rowconfigure(0, weight=1)
        self.bottomFrame.grid_rowconfigure(1, weight=1)
        self.bottomFrame.grid_columnconfigure(0, weight=1)

        self.laundry_form = LaundryForm(self, action_taken=self.paint) #this is self to access the vars in self
        self.laundry_form.grid(row=0, column=0, sticky='nsew')

        # divide the bottom frame by two divides top and bottom half again
        self.hostspot_module = HotSpot(self.bottomFrame, self.room_url)
        self.hostspot_module.grid(row=1,column=0,sticky='sw')

        self.machine_room = MachineRoom(self.bottomFrame, self.stats)
        self.machine_room.grid(row=0,column=0,sticky='wes')
        self.bottomFrame.grid_columnconfigure(0, weight=1)

        # self.testLabel = ttk.Label(self.bottomFrame, text="Nothing Entered Yet")
        # self.testLabel.pack(expand=True)
    def paint(self,*args):
        self.stats = self.laundry_form.stats
        self.room_url = self.laundry_form.url
        if self.hostspot_module:
            self.hostspot_module.destroy()
            self.machine_room.destroy()

        self.machine_room = MachineRoom(self.bottomFrame, self.stats)
        self.machine_room.grid(row=0,column=0,sticky='wse')

        self.hostspot_module = HotSpot(self.bottomFrame, self.room_url)
        self.hostspot_module.grid(row=1,column=0,sticky='sw')

if __name__ == "__main__":
    # start the Took Command Language / Tkinter Interpretor
    root = tk.Tk()
    # prevent the window from being resizable
    # root.resizable(width=False, height=False)
    # draw the MainApplication
    root.iconbitmap('washing-machine.ico')
    MainApplication(root).grid(row=0, column=0, sticky='nsew')
    # start the main loop
    root.mainloop()

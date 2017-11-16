from tkinter import *
import laundry_view

def submit_data(e):
    print("Data submitted")

def getting_start():
    window = Tk()
    window.title = "LaundryView Desktop"
    submit = Button(window, text="Submit")
    submit.pack()

    submit.bind('<Button-1>',submit_data)

    window.mainloop()

getting_start()

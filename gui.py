from tkinter import *
from tkinter import ttk
from tkinter import font
import threading


def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute


@thread
def count(txt1, a):
    a[0] = str(int(a[0])+1)
    a.append(1)
    txt1.set(a[0])
    root.after(1000, count, txt1, a)


def scroll(event):
    timer_list.yview_scroll(int(event.delta/120), "units")


def add_timer(a):
    a.append(-1)
    editing_window = Toplevel(root)
    editing_space = Canvas(editing_window, width=500, height=300, background='black', highlightthickness=0)
    editing_space.grid()
    button1 = Button(editing_space, text="THE POPUP")
    editing_space.create_window(100, 100, window=button1)

    type_setting = StringVar()
    type_setting.set("Timer")
    keepvalue = type_setting.get() # i mean, wtf dude why this works
    timer_setting = ttk.Combobox(editing_space, textvariable=keepvalue, values=('Timer', 'Alarm'), state='readonly')
    timer_setting.current(0)
#    editing_space.create_window(30, 30, window=alarm_setting)
    editing_space.create_window(90, 60, window=timer_setting)

# setting up space for widgets
root = Tk()
root.title("NERV")

frame = Frame(root, borderwidth=0, background='black', padx=0, pady=0)
frame.grid()

timer_list = Canvas(frame, width=650, height=600, scrollregion=(0, 0, 650, 1200), background='black', highlightthickness=0)
timer_list.grid(row=0, column=0)
scroll_x = Scrollbar(timer_list, orient="horizontal", command=timer_list.xview)
scroll_y = Scrollbar(timer_list, orient="vertical", command=timer_list.yview)
timer_list.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
timer_list.bind_all("<MouseWheel>", scroll)

sidebar = Canvas(frame, background='black', width=100, height=600, highlightthickness=0)
sidebar.grid(row=0, column=1)


intervals = ['10000000000']

text1 = StringVar()
text1.set(intervals[0])
century65 = font.Font(family="Century", name="Century65", size=65)
label = ttk.Label(timer_list, textvariable=text1, font=century65, background='black', foreground='white')
timer_list.create_window(300, 60, window=label)

timer_settings = PhotoImage(file="clock_settings50px.gif")
button_timer_settings = Button(timer_list, image=timer_settings, bg="black", bd=0, highlightthickness=0, activebackground='black')
timer_list.create_window(600, 65, window=button_timer_settings)

button = Button(timer_list, text="1234")
timer_list.create_window(400, 1100, window=button)

settings = PhotoImage(file="settings50px.gif")
button_settings = Button(sidebar, image=settings, bg="black", bd=0, highlightthickness=0, activebackground='black')
sidebar.create_window(50, 65, window=button_settings)

filter_icon = PhotoImage(file="filter50px.gif")
button_filter = Button(sidebar, image=filter_icon, bg="black", bd=0, highlightthickness=0, activebackground='black')
sidebar.create_window(50, 125, window=button_filter)

add_icon = PhotoImage(file="add50px.gif")
button_add = Button(sidebar, image=add_icon, command=lambda: add_timer(intervals), bg='black', bd=0, highlightthickness=0, activebackground='black')
sidebar.create_window(50, 185, window=button_add)


count(text1, intervals)

root.mainloop()

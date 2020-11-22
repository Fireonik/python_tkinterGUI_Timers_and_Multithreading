from tkinter import *
from tkinter import ttk
from tkinter import font
import threading


class EditingWindow:
    def __init__(self):
        self.__interval = [0]
        self.__signal = ""

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, val):
        self.__interval = val

    @property
    def signal(self):
        return self.__signal

    @signal.setter
    def signal(self, val):
        self.__signal = val


def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return execute


@thread
def count():
    global timers
    try:
        temp = timers[0].interval
        print(timers[0].interval)
        temp[0] -= 1
        timers[0].interval = temp
        print(timers[0].interval)
        if timers[0].interval[0] == 0:
            if timers[0].signal =='Ping1':
                from playsound import playsound
                playsound("Ping1.mp3")
    except Exception:
        pass
    root.after(1000, count)


def scroll(event):
    timer_list.yview_scroll(int(event.delta / 120), "units")





def add_timer(a):
    global timers
    timers.append(EditingWindow())

    editing_window = Toplevel(root)
    editing_window.resizable(False, False)
    editing_space = Frame(editing_window, width=300, height=300, background='black', highlightthickness=0)
    editing_space.grid(rows=10, columns=10)
    button1 = ttk.Button(editing_space, text="THE POPUP").grid(row=9, column=0)

    type_setting = StringVar()
    type_setting.set("")
    type_setting1 = type_setting.get()  # protection from garbage collector
    timer_setting = ttk.Combobox(editing_space, textvariable=type_setting1, values=("Timer", "Alarm"), state='readonly'
                                 , width=6)
    timer_setting.grid(row=0, column=0)

    days = IntVar()
    hours = IntVar()
    minutes = IntVar()
    seconds = IntVar()
    month = IntVar()
    day = IntVar()
    hour = IntVar()
    minute = IntVar()
    second = IntVar()
    signal = StringVar()
    month_list = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December')

    days_label = Label(editing_space, text='ddd', background='black', foreground='white')
    hours_label = Label(editing_space, text='hh', background='black', foreground='white')
    minutes_label = Label(editing_space, text='mm', background='black', foreground='white')
    seconds_label = Label(editing_space, text='ss', background='black', foreground='white')
    days_spinbox = ttk.Spinbox(editing_space, from_=0, to=365, textvariable=days, state='readonly', width=3)
    hours_spinbox = ttk.Spinbox(editing_space, from_=0, to=23, textvariable=hours, state='readonly', width=2)
    minutes_spinbox = ttk.Spinbox(editing_space, from_=0, to=59, textvariable=minutes, state='readonly',
                                  width=2)
    seconds_spinbox = ttk.Spinbox(editing_space, from_=0, to=59, textvariable=seconds, state='readonly',
                                  width=2)
    month_label = Label(editing_space, text='month', background='black', foreground='white')
    day_label = Label(editing_space, text='dd', background='black', foreground='white')
    hour_label = Label(editing_space, text='hh', background='black', foreground='white')
    minute_label = Label(editing_space, text='mm', background='black', foreground='white')
    second_label = Label(editing_space, text='ss', background='black', foreground='white')
    month_spinbox = ttk.Spinbox(editing_space, values=month_list, textvariable=month, state='readonly', width=10)

    signal_combobox = ttk.Combobox(editing_space, textvariable=signal, values=("Ping1", "Ping2", "Auratone", "Happyday", "Softchime"),
                                   state='readonly')

    days_label.grid(row=1, column=1)
    hours_label.grid(row=1, column=2)
    minutes_label.grid(row=1, column=3)
    seconds_label.grid(row=1, column=4)
    days_spinbox.grid(row=0, column=1)
    hours_spinbox.grid(row=0, column=2)
    minutes_spinbox.grid(row=0, column=3)
    seconds_spinbox.grid(row=0, column=4)
    month_label.grid(row=1, column=1)
    day_label.grid(row=1, column=2)
    hour_label.grid(row=1, column=3)
    minute_label.grid(row=1, column=4)
    second_label.grid(row=1, column=5)
    month_spinbox.grid(row=0, column=1)
    signal_combobox.grid(row=0, column=6, padx=5, pady=5)

    days_label.grid_forget()
    hours_label.grid_forget()
    minutes_label.grid_forget()
    seconds_label.grid_forget()
    days_spinbox.grid_forget()
    hours_spinbox.grid_forget()
    minutes_spinbox.grid_forget()
    seconds_spinbox.grid_forget()
    month_label.grid_forget()
    day_label.grid_forget()
    hour_label.grid_forget()
    minute_label.grid_forget()
    second_label.grid_forget()
    month_spinbox.grid_forget()

    def signal_setup(event):
        global timers
        timers[-1].signal = signal_combobox.get()

    def interval_setup(event):  # weird, why python doesn't see this argument is used
        global timers
        timers[-1].interval = [0]
        if timer_setting.get() == "Timer":
            month_label.grid_forget()
            day_label.grid_forget()
            hour_label.grid_forget()
            minute_label.grid_forget()
            second_label.grid_forget()
            month_spinbox.grid_forget()

            days_label.grid(row=1, column=1)
            hours_label.grid(row=1, column=2)
            minutes_label.grid(row=1, column=3)
            seconds_label.grid(row=1, column=4)
            days_spinbox.grid(row=0, column=1)
            hours_spinbox.grid(row=0, column=2)
            minutes_spinbox.grid(row=0, column=3)
            seconds_spinbox.grid(row=0, column=4)

            def interval_increment_seconds(event):
                try:
                    if int(seconds_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global timers
                temp = timers[-1].interval
                temp[0] += 1
                timers[-1].interval = temp

            def interval_increment_minutes(event):
                try:
                    if int(minutes_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global timers
                temp = timers[-1].interval
                temp[0] += 60
                timers[-1].interval = temp

            def interval_increment_hours(event):
                try:
                    if int(hours_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global timers
                temp = timers[-1].interval
                temp[0] += 3600
                timers[-1].interval = temp

            def interval_increment_days(event):
                try:
                    if int(days_spinbox.get()) == 365:
                        return
                except ValueError:
                    return
                global timers
                temp = timers[-1].interval
                temp[0] += 86400
                timers[-1].interval = temp

            def interval_decrement_seconds(event):
                global timers
                temp = timers[-1].interval
                temp[0] -= 1
                if temp[0] < 0:
                    temp[0] = 0
                timers[-1].interval = temp

            def interval_decrement_minutes(event):
                global timers
                temp = timers[-1].interval
                temp[0] -= 60
                if temp[0] < 0:
                    temp[0] = 0
                timers[-1].interval = temp

            def interval_decrement_hours(event):
                global timers
                temp = timers[-1].interval
                temp[0] -= 3600
                if temp[0] < 0:
                    temp[0] = 0
                timers[-1].interval = temp

            def interval_decrement_days(event):
                global timers
                temp = timers[-1].interval
                temp[0] -= 86400
                if temp[0] < 0:
                    temp[0] = 0
                timers[-1].interval = temp


            seconds_spinbox.bind('<<Increment>>', interval_increment_seconds)
            minutes_spinbox.bind('<<Increment>>', interval_increment_minutes)
            hours_spinbox.bind('<<Increment>>', interval_increment_hours)
            days_spinbox.bind('<<Increment>>', interval_increment_days)
            seconds_spinbox.bind('<<Decrement>>', interval_decrement_seconds)
            minutes_spinbox.bind('<<Decrement>>', interval_decrement_minutes)
            hours_spinbox.bind('<<Decrement>>', interval_decrement_hours)
            days_spinbox.bind('<<Decrement>>', interval_decrement_days)

        else:
            days_label.grid_forget()
            hours_label.grid_forget()
            minutes_label.grid_forget()
            seconds_label.grid_forget()
            days_spinbox.grid_forget()
            hours_spinbox.grid_forget()
            minutes_spinbox.grid_forget()
            seconds_spinbox.grid_forget()

            month_label.grid(row=1, column=1)
            day_label.grid(row=1, column=2)
            hour_label.grid(row=1, column=3)
            minute_label.grid(row=1, column=4)
            second_label.grid(row=1, column=5)
            month_spinbox.grid(row=0, column=1)

    timer_setting.bind('<<ComboboxSelected>>', interval_setup)
    signal_combobox.bind("<<ComboboxSelected>>", signal_setup)

timers = []
# setting up space for widgets
root = Tk()
root.title("NERV")

frame = Frame(root, borderwidth=0, background='black', padx=0, pady=0)
frame.grid()

timer_list = Canvas(frame, width=650, height=600, scrollregion=(0, 0, 650, 1200), background='black',
                    highlightthickness=0)
scroll_x = Scrollbar(timer_list, orient="horizontal", command=timer_list.xview)
scroll_y = Scrollbar(timer_list, orient="vertical", command=timer_list.yview)
sidebar = Canvas(frame, background='black', width=100, height=600, highlightthickness=0)

timer_list.grid(row=0, column=0)
timer_list.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
timer_list.bind_all("<MouseWheel>", scroll)
sidebar.grid(row=0, column=1)

intervals = ['10000000000']

text1 = StringVar()
text1.set(intervals[0])
century65 = font.Font(family="Century", name="Century65", size=65)
timer_settings = PhotoImage(file="clock_settings50px.gif")
settings = PhotoImage(file="settings50px.gif")
filter_icon = PhotoImage(file="filter50px.gif")
add_icon = PhotoImage(file="add50px.gif")

label = ttk.Label(timer_list, textvariable=text1, font=century65, background='black', foreground='white')
button_timer_settings = Button(timer_list, image=timer_settings, bg="black", bd=0, highlightthickness=0,
                               activebackground='black')
button = Button(timer_list, text="1234")
button_settings = Button(sidebar, image=settings, bg="black", bd=0, highlightthickness=0, activebackground='black')
button_filter = Button(sidebar, image=filter_icon, bg="black", bd=0, highlightthickness=0, activebackground='black')
button_add = Button(sidebar, image=add_icon, command=lambda: add_timer(intervals), bg='black', bd=0,
                    highlightthickness=0, activebackground='black')

timer_list.create_window(300, 60, window=label)
timer_list.create_window(600, 65, window=button_timer_settings)
timer_list.create_window(400, 1100, window=button)
sidebar.create_window(50, 65, window=button_settings)
sidebar.create_window(50, 125, window=button_filter)
sidebar.create_window(50, 185, window=button_add)

count()

root.mainloop()

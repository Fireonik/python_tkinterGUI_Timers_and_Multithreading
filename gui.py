from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from copy import deepcopy
from playsound import playsound
from PIL import ImageTk
import threading
import math


class Timer:
    def __init__(self):
        self.__interval = [0]
        self.__signal = ""
        self.__label = []
        self.__label_text = []

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self,
                 val):
        self.__interval = val

    @property
    def signal(self):
        return self.__signal

    @signal.setter
    def signal(self, val):
        self.__signal = val

    @property
    def label(self):

        return self.__label

    @label.setter
    def label(self, var):
        self.__label = var

    @property
    def label_text(self):
        return self.__label_text

    @label_text.setter
    def label_text(self, var):
        self.__label_text = var


def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()

    return execute


@thread
def sound_thread(filename):
    try:
        playsound(filename)
    except UnicodeDecodeError:
        pass


@thread
def message_thread():
    messagebox.showinfo(title="NERV", message="Timer expired")


def interval_formatted(i):
    global timers
    curr = timers[i].interval[0]
    days = str(math.floor(curr / 86400))
    if days == '0':
        days = ''
    elif int(days) < 10:
        days = "0" + days + ":"
    else:
        days += ":"
    hours = str(math.floor((curr % 86400) / 3600))
    if hours == '0':
        if days == '':
            hours = ''
        else:
            hours = '00:'
    elif int(hours) < 10:
        hours = "0" + hours + ":"
    else:
        hours += ':'
    minutes = str(math.floor(((math.floor(curr % 86400)) % 3600) / 60))
    if minutes == '0':
        if days == '' and hours == '':
            minutes = ''
        else:
            minutes = '00:'
    elif int(minutes) < 10:
        minutes = "0" + minutes + ":"
    else:
        minutes += ":"
    seconds = str(((curr % 86400) % 3600) % 60)
    if int(seconds) < 10:
        seconds = "0" + seconds
    return days + hours + minutes + seconds


@thread
def count():
    global timers, timer_list, timer_was_deleted, bodoni26
    size = len(timers)
    timer_list.config(scrollregion=(0, 0, 290, 100+40*size))
    print(size)
    for i in range(size):
        try:
            timers[i].interval[0] -= 1
            timers[i].label_text[0].set(interval_formatted(i))
            if timers[i].interval[0] == 0:
                sound_thread(timers[i].signal + ".mp3")
                message_thread()
                timers[i].label[0].destroy()
                del timers[i]
                timer_was_deleted = True
        except IndexError:
            pass
    if timer_was_deleted:
        for i in range(len(timers)):
            timers[i].label[0].destroy()
            del timers[i].label[0]
            temp_label = Label(timer_list, textvariable=timers[i].label_text[0], font=bodoni26, foreground='#622651')
            temp_label['bg'] = temp_label.master['bg']
            timers[i].label.append(temp_label)
            timer_list.create_window(260, 40 * i, window=timers[i].label[0], anchor='ne')
            timer_was_deleted = False
    root.after(1000, count)


@thread
def force_background():
    global window2, root

    # noinspection PyUnusedLocal
    def focus_handling(event):
        global window2, root
        root.focus_force()

    window2.geometry('290x200'+'+'+str(root.winfo_rootx())+'+'+str(root.winfo_rooty()))
    window2.bind('<FocusIn>', focus_handling)
    root.bind("<FocusIn>", focus_handling)
    window2.after(1, force_background)


def scroll_timer_list(event):
    timer_list.yview_scroll(int(event.delta / 120), "units")


def add_timer():
    global temp_window_data

    def confirm_add():
        global temp_window_data, timers, timer_list, bodoni26
        nonlocal editing_window
        if temp_window_data.interval[0] == 0:
            messagebox.showerror(title="NERV", message="Can't add timer without interval")
            editing_window.destroy()
        else:
            timers.append(Timer())
            timers[-1].interval = deepcopy(temp_window_data.interval)
            timers[-1].signal = deepcopy(temp_window_data.signal)

            temp_label_text = []
            temp_text = StringVar()
            temp_label_text.append(temp_text)
            temp_label_text[0].set(interval_formatted(-1))
            timers[-1].label_text = temp_label_text
            temp_label = Label(timer_list, textvariable=temp_label_text, font=bodoni26, foreground='#622651')
            temp_label['bg'] = temp_label.master['bg']
            timers[-1].label.append(temp_label)
            timer_list.create_window(260, 40*(len(timers)-1), window=timers[-1].label, anchor='ne')

            temp_window_data.interval[0] = 0
            temp_window_data.signal = ""
            editing_window.destroy()

    editing_window = Toplevel(root)
    editing_window.resizable(False, False)
    editing_window.attributes("-topmost", True)
    editing_space = Frame(editing_window)
    editing_space.grid(rows=10, columns=10)
    ttk.Button(editing_space, text="Confirm", command=confirm_add).grid(row=0, column=9)
    type_setting = StringVar()
    type_setting.set("")
    type_setting1 = type_setting.get()  # protection from garbage collector
    timer_setting = ttk.Combobox(editing_space, textvariable=type_setting1, values=("Timer", "Alarm"), state='readonly',
                                 width=6)
    timer_setting.grid(row=0, column=0)

    days, hours, minutes, seconds, month, day, hour, minute, second = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    signal = StringVar()
    month_list = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December')

    days_label = Label(editing_space, text='ddd')
    hours_label = Label(editing_space, text='hh')
    minutes_label = Label(editing_space, text='mm')
    seconds_label = Label(editing_space, text='ss')
    days_spinbox = ttk.Spinbox(editing_space, from_=0, to=365, textvariable=days, state='readonly', width=3)
    hours_spinbox = ttk.Spinbox(editing_space, from_=0, to=23, textvariable=hours, state='readonly', width=2)
    minutes_spinbox = ttk.Spinbox(editing_space, from_=0, to=59, textvariable=minutes, state='readonly',
                                  width=2)
    seconds_spinbox = ttk.Spinbox(editing_space, from_=0, to=59, textvariable=seconds, state='readonly',
                                  width=2)
    month_label = Label(editing_space, text='month')
    day_label = Label(editing_space, text='dd')
    hour_label = Label(editing_space, text='hh')
    minute_label = Label(editing_space, text='mm')
    second_label = Label(editing_space, text='ss')
    month_spinbox = ttk.Spinbox(editing_space, values=month_list, textvariable=month, state='readonly', width=10)
    # noinspection SpellCheckingInspection
    signal_combobox = ttk.Combobox(editing_space, textvariable=signal, values=("Ping1", "Ping2", "Auratone", "Happyday", "Softchime"),
                                   state='readonly')
    signal_combobox.grid(row=0, column=6, padx=5, pady=5)

    # noinspection PyUnusedLocal
    def signal_setup(event):
        global temp_window_data
        temp_window_data.signal = signal_combobox.get()

    # noinspection PyUnusedLocal
    def interval_setup(event):
        global temp_window_data
        temp_window_data.interval = [0]
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

            # noinspection PyUnusedLocal
            def interval_increment_seconds(event1):
                try:
                    if int(seconds_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global temp_window_data
                temp_window_data.interval[0] += 1

            # noinspection PyUnusedLocal
            def interval_increment_minutes(event1):
                try:
                    if int(minutes_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global temp_window_data
                temp_window_data.interval[0] += 60

            # noinspection PyUnusedLocal
            def interval_increment_hours(event1):
                try:
                    if int(hours_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global temp_window_data
                temp_window_data.interval[0] += 3600

            # noinspection PyUnusedLocal
            def interval_increment_days(event1):
                try:
                    if int(days_spinbox.get()) == 365:
                        return
                except ValueError:
                    return
                global temp_window_data
                temp_window_data.interval[0] += 86400

            # noinspection PyUnusedLocal
            def interval_decrement_seconds(event1):
                global temp_window_data
                temp_window_data.interval[0] -= 1
                if temp_window_data.interval[0] < 0:
                    temp_window_data.interval[0] = 0

            # noinspection PyUnusedLocal
            def interval_decrement_minutes(event1):
                global temp_window_data
                temp_window_data.interval[0] -= 60
                if temp_window_data.interval[0] < 0:
                    temp_window_data.interval[0] = 0

            # noinspection PyUnusedLocal
            def interval_decrement_hours(event1):
                global temp_window_data
                temp_window_data.interval[0] -= 3600
                if temp_window_data.interval[0] < 0:
                    temp_window_data.interval[0] = 0

            # noinspection PyUnusedLocal
            def interval_decrement_days(event1):
                global temp_window_data
                temp_window_data.interval[0] -= 86400
                if temp_window_data.interval[0] < 0:
                    temp_window_data.interval[0] = 0

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


root = Tk()

# global variables
timers = []
timer_was_deleted = False
temp_window_data = Timer()
temp_window_data.interval[0] = 0
settings = PhotoImage(file="settings24px.gif")
add_icon = PhotoImage(file="add24.gif")
file = ImageTk.PhotoImage(file="C:\\Users\\Clarity\\Desktop\\SimonRed1.png")
bodoni26 = font.Font(family="Bodoni MT", name="Bodoni26", size=26)

# main window setup
root.title("NERV")
root.resizable(False, False)
root.attributes("-topmost", True)
root.wm_attributes('-transparentcolor', root['bg'])
root_frame = Frame(root, borderwidth=0, padx=0, pady=0)
root_frame.grid()
timer_list = Canvas(root_frame, width=265, height=200, scrollregion=(0, 0, 265, 1200), highlightthickness=0)
scroll_x = Scrollbar(timer_list, orient="horizontal", command=timer_list.xview)
scroll_y = Scrollbar(timer_list, orient="vertical", command=timer_list.yview)
timer_list.grid(row=0, column=0, sticky=(N, W, E, S))
timer_list.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
timer_list.bind_all("<MouseWheel>", scroll_timer_list)
sidebar = Canvas(root_frame, width=25, height=200, highlightthickness=0)
sidebar.grid(row=0, column=1)
button_settings = Button(sidebar, image=settings, bd=0, highlightthickness=0)
button_add = Button(sidebar, image=add_icon, command=lambda: add_timer(), bd=0,)
sidebar.create_window(10, 15, window=button_settings)
sidebar.create_window(10, 40, window=button_add)

# background setup
window2 = Toplevel()
window2.overrideredirect(True)
window2.attributes("-topmost", True)
bg_frame = Frame(window2)
bg_frame.grid()
bg_canvas = Canvas(bg_frame, width=290, height=205, highlightthickness=0, bd=0)
bg_canvas.grid(row=0, column=0, sticky='nw')
bg_canvas.create_image(140, 95, image=file)

force_background()
count()
root.mainloop()

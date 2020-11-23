from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from copy import deepcopy
from playsound import playsound
import threading


class EditingWindow:
    def __init__(self):
        self.__interval = [0]
        self.__signal = ""
        self.__label = []
        self.__label_text = []

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


@thread
def count():
    global timers, text1, timer_list
    size = len(timers)
    timer_list.config(scrollregion=(0, 0, 285, 100+40*size))
    print(size)
    for i in range(size):
        try:
            timers[i].interval[0] -= 1
            print(timers[i].interval)
            a = StringVar()
            a.set(str(timers[i].interval[0]))
            timers[i].label_text[0].set(str(timers[i].interval[0]))
            if timers[i].interval[0] == 0:
                sound_thread(timers[i].signal + ".mp3")
                message_thread()
                del timers[i]
        except IndexError:
            pass
    root.after(1000, count)


def scroll(event):
    timer_list.yview_scroll(int(event.delta / 120), "units")


def add_timer():
    global temp_window_data

    def confirm_add():
        global temp_window_data, timers, timer_list, century30
        nonlocal editing_window
        if temp_window_data.interval[0] == 0:
            messagebox.showerror(title="NERV", message="Can't add timer without interval")
            editing_window.destroy()
        else:
            timers.append(EditingWindow())
            timers[-1].interval = deepcopy(temp_window_data.interval)
            timers[-1].signal = deepcopy(temp_window_data.signal)
            temp_label_text = []
            temp_text = StringVar()
            temp_label_text.append(temp_text)

            temp_label_text[0].set(str(timers[-1].interval[0]))
            timers[-1].label_text = temp_label_text
            temp_label = ttk.Label(timer_list, textvariable=temp_label_text, font=century30)
            timers[-1].label.append(temp_label)
            timer_list.create_window(125, 20+40*(len(timers)-1), window=timers[-1].label)
            temp_window_data.interval[0] = 0
            temp_window_data.signal = ""
            editing_window.destroy()

    editing_window = Toplevel(root)
    editing_window.resizable(False, False)
    editing_space = Frame(editing_window, width=300, height=300, highlightthickness=0)
    editing_space.grid(rows=10, columns=10)
    ttk.Button(editing_space, text="Confirm", command=confirm_add).grid(row=0, column=9)

    type_setting = StringVar()
    type_setting.set("")
    type_setting1 = type_setting.get()  # protection from garbage collector
    timer_setting = ttk.Combobox(editing_space, textvariable=type_setting1, values=("Timer", "Alarm"), state='readonly',
                                 width=6)
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
        global temp_window_data
        temp_window_data.signal = signal_combobox.get()

    def interval_setup(event):  # weird, why python doesn't see this argument is used
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

            def interval_increment_seconds(event):
                try:
                    if int(seconds_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global temp_window_data
                temp_window_data.interval[0] += 1

            def interval_increment_minutes(event):
                try:
                    if int(minutes_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global temp_window_data
                temp_window_data.interval[0] += 60

            def interval_increment_hours(event):
                try:
                    if int(hours_spinbox.get()) == 59:
                        return
                except ValueError:
                    return
                global temp_window_data
                temp_window_data.interval[0] += 3600

            def interval_increment_days(event):
                try:
                    if int(days_spinbox.get()) == 365:
                        return
                except ValueError:
                    return
                global temp_window_data
                temp_window_data.interval[0] += 86400

            def interval_decrement_seconds(event):
                global temp_window_data
                temp_window_data.interval[0] -= 1
                if temp_window_data.interval[0] < 0:
                    temp_window_data.interval[0] = 0

            def interval_decrement_minutes(event):
                global temp_window_data
                temp_window_data.interval[0] -= 60
                if temp_window_data.interval[0] < 0:
                    temp_window_data.interval[0] = 0

            def interval_decrement_hours(event):
                global temp_window_data
                temp_window_data.interval[0] -= 3600
                if temp_window_data.interval[0] < 0:
                    temp_window_data.interval[0] = 0

            def interval_decrement_days(event):
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


timers = []

temp_window_data = EditingWindow()
temp_window_data.interval[0] = 0
# setting up space for widgets
root = Tk()
root.title("NERV")

frame = Frame(root, borderwidth=0, padx=0, pady=0)
frame.grid()

timer_list = Canvas(frame, width=285, height=200, scrollregion=(0, 0, 285, 1200), highlightthickness=0)
scroll_x = Scrollbar(timer_list, orient="horizontal", command=timer_list.xview)
scroll_y = Scrollbar(timer_list, orient="vertical", command=timer_list.yview)
sidebar = Canvas(frame, width=25, height=200, highlightthickness=0)

timer_list.grid(row=0, column=0, sticky=NW)
timer_list.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
timer_list.bind_all("<MouseWheel>", scroll)
sidebar.grid(row=0, column=1)


century30 = font.Font(family="Century", name="Century30", size=30)
timer_settings = PhotoImage(file="timer_settings25px.gif")
settings = PhotoImage(file="settings24px.gif")
add_icon = PhotoImage(file="add24.gif")


button_timer_settings = Button(timer_list, image=timer_settings, bd=0, highlightthickness=0)
button_settings = Button(sidebar, image=settings, bd=0, highlightthickness=0)
button_add = Button(sidebar, image=add_icon, command=lambda: add_timer(), bd=0,)


timer_list.create_window(260, 21, window=button_timer_settings)
sidebar.create_window(10, 20, window=button_settings)
sidebar.create_window(10, 55, window=button_add)

count()

root.mainloop()

from tkinter import *
from tkinter import font
from tkinter import messagebox
from copy import deepcopy
from playsound import playsound
from PIL import ImageTk
import threading
import math
import time
import pickle
import datetime
import sys


class Timer:
    last_id = 0
    last_shortest = 0
    expired_timers = []

    def __init__(self):
        self.interval = 0
        self.name_label = []
        self.name_label_text = StringVar()
        self.signal = 'Auratone'
        self.label = []
        self.label_text = StringVar()
        self.type = ''
        self.time_point = {}
        self.button = []
        self.id = 0
        self.name = ''
        self.time_point_of_save = []


def generate_id():
    Timer.last_id += 1
    return deepcopy(Timer.last_id)


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
def message_thread(name=None):
    if name is not None:
        messagebox.showinfo(title="NERV", message="Timer " + name +" expired")
    else:
        messagebox.showinfo(title="NERV", message="Timer expired")


def delete(id_):
    for index in range(len(timers)):
        if timers[index].id == id_:
            timers[index].label[0].destroy()
            timers[index].button[0].destroy()
            timers[index].name_label[0].destroy()
            del timers[index]
            refresh_timer_list()
            return


def filter_setting():
    def set_state(a):
        global filter_state
        filter_state = a
        refresh_timer_list()
        filter_setting_window.destroy()

    filter_setting_window = Toplevel()
    filter_setting_window.resizable(False, False)
    filter_setting_window.attributes("-topmost", True)
    filter_setting_window.geometry('309x39' + '+' + str(root.winfo_rootx() + 60) + '+' + str(root.winfo_rooty() + 50))
    Button(filter_setting_window, text="Timers", command=lambda: set_state('Timer'), font=font.Font(family='Bodoni MT', size=14), foreground='#622651').grid(row=0, column=0, ipadx=10)
    Button(filter_setting_window, text="Everything", command=lambda: set_state('Everything'),  font=font.Font(family='Bodoni MT', size=14), foreground='#622651').grid(row=0, column=1, ipadx=10)
    Button(filter_setting_window, text="Alarms", command=lambda: set_state('Alarm'),  font=font.Font(family='Bodoni MT', size=14), foreground='#622651').grid(row=0, column=2, ipadx=10)

def time_point_into_interval(month, d, h, minute, s):
    t = time.localtime()
    year_is_this_one = True
    # order is important here, laziness is exploited
    if month - t.tm_mon < 0 or month - t.tm_mon == 0 and d - t.tm_mday < 0 or d - t.tm_mday == 0 and h - t.tm_hour < 0 or h - t.tm_hour == 0 and minute - t.tm_min < 0 or minute - t.tm_min == 0 and s - t.tm_sec < 0:
        year_is_this_one = False
    alarm_year = t.tm_year if year_is_this_one else t.tm_year + 1

    end = datetime.datetime(alarm_year, month, d, h, minute, s)
    begin = datetime.datetime.today()
    return (end - begin).total_seconds()


def refresh_timer_list():

    def the_shortest():
        curr_interval = timers[0].interval if timers[0].type == 'Timer' else time_point_into_interval(timers[0].time_point.get('month'), timers[0].time_point.get('day'), timers[0].time_point.get('hour'), timers[0].time_point.get('minute'), timers[0].time_point.get('second'))
        index = 0
        for i in range(len(timers)):
            month = timers[i].time_point.get('month')
            day = timers[i].time_point.get('day')
            hour = timers[i].time_point.get('hour')
            minute = timers[i].time_point.get('minute')
            second = timers[i].time_point.get('second')
            if timers[i].type == 'Timer' and timers[i].interval < curr_interval:
                curr_interval = timers[i].interval
                index = i
            elif timers[i].type == 'Alarm' and time_point_into_interval(month, day, hour, minute, second) < curr_interval:
                curr_interval = time_point_into_interval(month, day, hour, minute, second)
                index = i
        return index

    def actually_just_refresh():
        for j in range(len(timers)):
            timer_list.create_window(250, (40 * j) + 24, window=timers[j].name_label[0])
            timer_list.create_window(550, 40 * j, window=timers[j].label[0], anchor='ne')
            timer_list.create_window(570, (40 * j) + 15, window=timers[j].button[0], anchor='ne')

    def sort_by_type():  # it is so brutal because tkinter cant temporarily remove widget from canvas
        # get space to put stuff into
        canvas_size = 100+40*len(timers)
        timer_list.config(scrollregion=(0, 0, 575, 2 * canvas_size))

        # put everything somewhere else
        for i in range(len(timers)):
            timer_list.create_window(550, canvas_size + (40 * i), window=timers[i].label[0], anchor='ne')
            timer_list.create_window(570, canvas_size + ((40 * i) + 15), window=timers[i].button[0], anchor='ne')

        # put chosen type back
        index = 0
        for i in range(len(timers)):
            timer_list.create_window(550, 40 * index, window=timers[i].label[0], anchor='ne')
            timer_list.create_window(570, (40 * index) + 15, window=timers[i].button[0], anchor='ne')
            index += 1

        # put the other type back
        for i in range(len(timers)):
            if filter_state != timers[i].type:
                timer_list.create_window(550, 40 * index, window=timers[i].label[0], anchor='ne')
                timer_list.create_window(570, (40 * index) + 15, window=timers[i].button[0], anchor='ne')
                index += 1

        # get rid of unnecessary space
        timer_list.config(scrollregion=(0, 0, 575, canvas_size))

    if len(timers) == 0:
        return

    if filter_state == 'Everything':
        actually_just_refresh()
    else:
        sort_by_type()
    try:
        timers[Timer.last_shortest].label[0]['foreground'] = '#622651'
    except IndexError:
        pass
    Timer.last_shortest = the_shortest()
    timers[Timer.last_shortest].label[0]['foreground'] = 'black'


def timer_termination(index):
    global timer_was_deleted, volume_is_on
    if volume_is_on:
        sound_thread('lab2/sound_signals/' + timers[index].signal + '.mp3')
        message_thread()
    timers[index].label[0].destroy()
    timers[index].button[0].destroy()
    del timers[index]
    timer_was_deleted = True


def timer_expiry(index):
    Timer.expired_timers.append(timers[index].name)
    del timers[index]


@thread
def count():
    def one_thread_is_enough():
        global timers, timer_list, timer_was_deleted, bodoni26, volume_is_on

        def the_time_has_come(ind):
            try:
                if timers[ind].type == 'Timer':
                    timers[ind].interval -= 1
                    timers[ind].label_text.set(interval_formatted(ind))
                    if timers[ind].interval == 0:
                        return True
                    return False
                else:
                    curr = time.localtime()
                    alarm = timers[ind].time_point
                    if curr.tm_mon == alarm.get('month') and curr.tm_mday == alarm.get('day') and curr.tm_hour == alarm.get('hour') and curr.tm_min == alarm.get('minute') and curr.tm_sec == alarm.get('second'):
                        return True
                    return False
            except IndexError:
                pass

        for i in range(len(Timer.expired_timers)):
            message_thread(Timer.expired_timers[i])
        Timer.expired_timers.clear()

        size = len(timers)
        timer_list.config(scrollregion=(0, 0, 575, 100+40*size))
        if size > 0:
            for i in range(size):
                try:
                    if the_time_has_come(i):
                        timer_termination(i)
                except IndexError:
                    pass
        if timer_was_deleted:
            refresh_timer_list()
            timer_was_deleted = False
        root.after(1000, one_thread_is_enough)
    one_thread_is_enough()


def focus_handling(event=None):
    global window2, root
    root.focus_force()


def minimize_bg(event=None):
    global window2
    window2.withdraw()


def unminimize_bg(event=None):
    global window2, root
    window2.deiconify()
    root.deiconify()


def force_background(event=None):
    global window2, root
    x = deepcopy(str(root.winfo_rootx()))
    y = deepcopy(str(root.winfo_rooty()))
    window2.geometry('600x200' + '+' + x + '+' + y)
    del x, y


def scroll_timer_list(event):
    timer_list.yview_scroll(int(event.delta / 120), "units")


def interval_formatted(i):
    global timers
    curr = timers[i].interval
    temp = [str(math.floor(curr / 86400)), str(math.floor((curr % 86400) / 3600)),
            str(math.floor(((math.floor(curr % 86400)) % 3600) / 60)), str(((curr % 86400) % 3600) % 60)]
    stop = False
    for i in range(3):
        if temp[i] == '0' and stop is False:
            temp[i] = ''
        else:
            stop = True
            if int(temp[i]) < 10:
                temp[i] = "0" + temp[i]
            temp[i] += ":"
    if int(temp[3]) < 10:
        temp[3] = '0' + temp[3]
    return temp[0] + temp[1] + temp[2] + temp[3]


def time_point_formatted(mon, d, h, minute, s):
    a = [mon, d, h, minute, s]
    for ind in range(5):
        if int(a[ind]) < 10:
            a[ind] = '0' + a[ind]
    return a[0] + '.' + a[1] + ' ' + a[2] + ":" + a[3] + ':' + a[4]


def add():
    def move_to_timer_setup(event=None):
        timer_setup_window.destroy()
        timer_setup()

    def move_to_alarm_setup(event=None):
        timer_setup_window.destroy()
        alarm_setup()

    timer_setup_window = Toplevel()
    timer_setup_window.resizable(False, False)
    timer_setup_window.attributes("-topmost", True)
    timer_setup_window.geometry('169x39' + '+' + str(root.winfo_rootx()+60) + '+' + str(root.winfo_rooty()+50))
    Button(timer_setup_window, text="Timer", command=move_to_timer_setup, font=font.Font(family='Bodoni MT', size=14), foreground='#622651').grid(row=0, column=0, ipadx=10)
    Button(timer_setup_window, text="Alarm", command=move_to_alarm_setup, font=font.Font(family='Bodoni MT', size=14), foreground='#622651').grid(row=0, column=1, ipadx=10)


def alarm_setup():
    def confirm_add(event=None):
        m = int(month.get())
        d = int(day.get())
        if m in {4, 6, 9, 11} and d == 31 or m == 2 and d > 29:
            messagebox.showwarning(title='NERV', message='Invalid day number')
            return
        timers.append(Timer())
        timers[-1].type = 'Alarm'
        timers[-1].name = str(name.get())
        timers[-1].name_label_text.set(name.get())
        timers[-1].name_label.append(Label(timer_list, textvariable=timers[-1].name_label_text, font=bodoni14, foreground='green'))

        timers[-1].id = generate_id()
        timers[-1].time_point['month'] = int(month.get())
        timers[-1].time_point['day'] = int(day.get())
        timers[-1].time_point['hour'] = int(hour.get())
        timers[-1].time_point['minute'] = int(minute.get())
        timers[-1].time_point['second'] = int(second.get())
        timers[-1].signal = signal.get()
        timers[-1].label_text.set(time_point_formatted(month.get(), day.get(), hour.get(), minute.get(), second.get()))
        timers[-1].label.append(Label(timer_list, textvariable=timers[-1].label_text, font=bodoni26, foreground='#622651'))
        the_id = deepcopy(timers[-1].id)
        timers[-1].button.append(Button(timer_list, image=remove_icon, command=lambda: delete(the_id), relief='flat', highlightthickness=1, bd=0))
        timer_list.create_window(250, (40 * (len(timers) - 1) + 24), window=timers[-1].name_label[0])
        timer_list.create_window(540, 40 * (len(timers) - 1), window=timers[-1].label[0], anchor='ne')
        timer_list.create_window(560, (40 * (len(timers) - 1)) + 15, window=timers[-1].button[0], anchor='ne')
        nonlocal alarm_setup_window
        alarm_setup_window.destroy()
        refresh_timer_list()

    alarm_setup_window = Toplevel()
    alarm_setup_window.resizable(False, False)
    alarm_setup_window.attributes("-topmost", True)
    alarm_setup_window.geometry('660x60' + '+' + str(root.winfo_rootx() + 50) + '+' + str(root.winfo_rooty() + 50))
    bodoni14 = font.Font(family="Bodoni MT", size=14)
    Label(alarm_setup_window, text='mon', font=bodoni14, foreground='#622651').grid(row=0, column=1)
    Label(alarm_setup_window, text='day', font=bodoni14, foreground='#622651').grid(row=0, column=2)
    Label(alarm_setup_window, text='hour', font=bodoni14, foreground='#622651').grid(row=0, column=3)
    Label(alarm_setup_window, text='min', font=bodoni14, foreground='#622651').grid(row=0, column=4)
    Label(alarm_setup_window, text='sec', font=bodoni14, foreground='#622651').grid(row=0, column=5)
    Label(alarm_setup_window, text='signal', font=bodoni14, foreground='#622651').grid(row=0, column=6, sticky='w')
    Label(alarm_setup_window, text='name', font=bodoni14, foreground='#622651').grid(row=0, column=0, sticky='w')
    name = Entry(alarm_setup_window, font=bodoni14, foreground='#622651')
    name.grid(row=1, column=0)
    month = Spinbox(alarm_setup_window, from_=1, to=12, width=2, font=bodoni14, state='readonly', foreground='#622651')
    month.grid(row=1, column=1)
    day = Spinbox(alarm_setup_window, from_=1, to=31, width=2, font=bodoni14, state='readonly', foreground='#622651')
    day.grid(row=1, column=2)
    hour = Spinbox(alarm_setup_window, from_=0, to=23, width=2, font=bodoni14, state='readonly', foreground='#622651')
    hour.grid(row=1, column=3)
    minute = Spinbox(alarm_setup_window, from_=0, to=59, width=2, font=bodoni14, state='readonly', foreground='#622651')
    minute.grid(row=1, column=4)
    second = Spinbox(alarm_setup_window, from_=0, to=59, width=2, font=bodoni14, state='readonly', foreground='#622651')
    second.grid(row=1, column=5)
    signal = Spinbox(alarm_setup_window, values=("Auratone", "Softchime", "Happyday", "Ping1", "Ping2"), font=bodoni14, state='readonly', foreground='#622651')
    signal.grid(row=1, column=6)
    Button(alarm_setup_window, command=confirm_add, text="OK", font=font.Font(family='Bodoni MT', size=16)).grid(row=0, ipady=4, column=7, rowspan=2, columnspan=2, sticky='s', padx=5, ipadx=15)


def timer_setup():
    def confirm_add(event=None):
        interval = eval(days.get())*86400 + eval(hours.get())*3600 + eval(minutes.get())*60 + eval(seconds.get())
        if interval <= 0:
            messagebox.showwarning(title='NERV', message='Invalid interval')
            return

        timers.append(Timer())
        timers[-1].type = 'Timer'
        timers[-1].name = str(name.get())
        timers[-1].name_label_text.set(name.get())
        timers[-1].name_label.append(Label(timer_list, textvariable=timers[-1].name_label_text, font=bodoni14, foreground='green'))
        timers[-1].id = generate_id()
        timers[-1].interval = interval
        timers[-1].signal = signal.get()
        timers[-1].label_text.set(interval_formatted(-1))
        timers[-1].label.append(Label(timer_list, textvariable=timers[-1].label_text, font=bodoni26, foreground='#622651'))
        the_id = deepcopy(timers[-1].id)
        timers[-1].button.append(Button(timer_list, image=remove_icon, command=lambda: delete(the_id), relief='flat', highlightthickness=1, bd=0))
        timer_list.create_window(250, (40 * (len(timers) - 1) + 24), window=timers[-1].name_label[0])
        timer_list.create_window(350, 40 * (len(timers) - 1), window=timers[-1].label[0], anchor='ne')
        timer_list.create_window(370, (40 * (len(timers) - 1)) + 15, window=timers[-1].button[0], anchor='ne')
        timer_setup_window.destroy()
        refresh_timer_list()

    timer_setup_window = Toplevel()
    timer_setup_window.resizable(False, False)
    timer_setup_window.attributes("-topmost", True)
    timer_setup_window.geometry('620x58' + '+' + str(root.winfo_rootx() + 50) + '+' + str(root.winfo_rooty() + 50))
    bodoni14 = font.Font(family="Bodoni MT", size=14)
    name = Entry(timer_setup_window, font=bodoni14, foreground='#622651')
    name.grid(row=1, column=0)
    days = Spinbox(timer_setup_window, from_=0, to=365, width=3, font=bodoni14, state='readonly', foreground='#622651')
    days.grid(row=1, column=1, padx=1)
    hours = Spinbox(timer_setup_window, from_=0, to=23, width=2, font=bodoni14, state='readonly', foreground='#622651')
    hours.grid(row=1, column=2)
    minutes = Spinbox(timer_setup_window, from_=0, to=59, width=2, font=bodoni14, state='readonly', foreground='#622651')
    minutes.grid(row=1, column=3)
    seconds = Spinbox(timer_setup_window, from_=0, to=59, width=2, font=bodoni14, state='readonly', foreground='#622651')
    seconds.grid(row=1, column=4)
    signal = Spinbox(timer_setup_window, values=('Plan', 'TimerExpired', 'AlarmWentOff', "Auratone", "Softchime", "Happyday", "Ping1", "Ping2"), font=bodoni14, state='readonly', foreground='#622651')
    signal.grid(row=1, column=5)
    Button(timer_setup_window, command=confirm_add, text="OK", font=font.Font(family='Bodoni MT', size=16)).grid(row=0, column=6, rowspan=2, columnspan=2, ipady=6, padx=3, ipadx=15)
    Label(timer_setup_window, text='name', font=bodoni14, foreground='#622651').grid(row=0, column=0, sticky='w')
    Label(timer_setup_window, text='ddd', font=bodoni14, foreground='#622651').grid(row=0, column=1, sticky='w')
    Label(timer_setup_window, text='hh', font=bodoni14, foreground='#622651').grid(row=0, column=2, sticky='w')
    Label(timer_setup_window, text='mm', font=bodoni14, foreground='#622651').grid(row=0, column=3, sticky='w')
    Label(timer_setup_window, text='ss', font=bodoni14, foreground='#622651').grid(row=0, column=4, sticky='w')
    Label(timer_setup_window, text='signal', font=bodoni14, foreground='#622651').grid(row=0, column=5, sticky='w')


def save():
    if len(timers) == 0:
        with open('lab2/save.bin', 'wb'):
            pass
        sys.exit()

    # tkinter widgets can not be pickled, fortunately we don't have to save them
    for i in range(len(timers)):
        if timers[i].type == 'Timer':
            timers[i].time_point['save'] = datetime.datetime.today()
        else:
            month = timers[i].time_point.get('month')
            day = timers[i].time_point.get('day')
            hour = timers[i].time_point.get('hour')
            minute = timers[i].time_point.get('minute')
            second = timers[i].time_point.get('second')
            timers[i].interval = time_point_into_interval(month, day, hour, minute, second)
            timers[i].time_point_of_save.append(datetime.datetime.today())

        timers[i].label.clear()
        timers[i].name_label.clear()
        del timers[i].label_text
        del timers[i].name_label_text
        timers[i].button.clear()

    data = [timers, timer_was_deleted, filter_state]
    try:
        with open('lab2/save.bin', 'wb') as save_file:
            pickle.dump(data, save_file)
            sys.exit()
    except pickle.PicklingError:
        sys.exit(1)


def load():
    global timers, timer_was_deleted, filter_state
    bodoni14 = font.Font(family="Bodoni MT", size=14)

    try:
        with open('lab2/save.bin', 'rb') as save_file:
            data = pickle.load(save_file)
    except IOError:
        return
    except pickle.UnpicklingError:
        return
    except EOFError:
        return

    # loading the data
    timers = data[0]
    timer_was_deleted = data[1]

    # setting up tkinter widgets
    for i in range(len(timers)):
        timers[i].label_text = StringVar()
        timers[i].name_label_text = StringVar()
        timers[i].name_label_text.set(timers[i].name)
        if timers[i].type == 'Timer':
            timers[i].label_text.set(interval_formatted(i))
        else:
            month = str(timers[i].time_point.get('month'))
            day = str(timers[i].time_point.get('day'))
            hour = str(timers[i].time_point.get('hour'))
            minute = str(timers[i].time_point.get('minute'))
            second = str(timers[i].time_point.get('second'))
            timers[i].label_text.set(time_point_formatted(month, day, hour, minute, second))

        timers[i].label.append(Label(timer_list, textvariable=timers[i].label_text, font=bodoni26, foreground='#622651'))
        very_sad_icon = PhotoImage(file='lab2/icons/very_sad_Icon.gif')
        timers[i].button.append(Button(timer_list, image=very_sad_icon, relief='flat', highlightthickness=1, bd=0))
        timers[i].name_label.append(Label(timer_list, textvariable=timers[i].name_label_text, font=bodoni14, foreground='green'))

    for i in range(len(timers)):
        if timers[i].type == 'Timer':
            time_passed = (datetime.datetime.today() - timers[i].time_point.get('save')).seconds
            timers[i].interval -= time_passed
            if timers[i].interval <= 0:
                timer_expiry(i)
        else:
            time_passed = (datetime.datetime.today() - timers[i].time_point_of_save[0]).seconds
            timers[i].interval -= time_passed
            if timers[i].interval <= 0:
                timer_expiry(i)
    # display widgets
    filter_state = 'Everything'
    refresh_timer_list()
    filter_state = data[2]
    refresh_timer_list()


def change_volume_state():
    global volume_is_on, volume_state_icon, button_volume_state, sidebar
    volume_state_icon = PhotoImage(file='lab2/icons/volume_off.gif') if volume_is_on else PhotoImage(file='lab2/icons/volume_on.gif')
    volume_is_on = not volume_is_on
    button_volume_state = Button(sidebar, image=volume_state_icon, command=change_volume_state, bd=0)
    sidebar.create_window(14, 65, window=button_volume_state)


def delete_all():
    for i in range(len(timers)):
        timers[i].label[0].destroy()
        timers[i].button[0].destroy()
        timers[i].name_label[0].destroy()
    timers.clear()


root = Tk()

# global variables
timers = []
timer_was_deleted = False
filter_state = 'Everything'
add_icon = PhotoImage(file="lab2/icons/add24.gif")
remove_icon = PhotoImage(file='lab2/icons/remove.gif')
filter_icon = PhotoImage(file='lab2/icons/filter.gif')
delete_bin_icon = PhotoImage(file='lab2/icons/delete_bin.gif')
volume_state_icon = PhotoImage(file='lab2/icons/volume_on.gif')
volume_is_on = True
file = ImageTk.PhotoImage(file="lab2/SimonRed1.png")
bodoni26 = font.Font(family="Bodoni MT", name="Bodoni26", size=26)


# main window setup
root.title("NERV")
root.resizable(False, False)
root.attributes("-topmost", True)
root.wm_attributes('-transparentcolor', root['bg'])
root_frame = Frame(root, borderwidth=0, padx=0, pady=0)
root_frame.grid()
timer_list = Canvas(root_frame, width=575, height=200, scrollregion=(0, 0, 575, 1200), highlightthickness=0)
scroll_y = Scrollbar(timer_list, orient="vertical", command=timer_list.yview)
timer_list.grid(row=0, column=0, sticky=(N, W, E, S))
timer_list.configure(yscrollcommand=scroll_y.set)
timer_list.bind_all("<MouseWheel>", scroll_timer_list)
sidebar = Canvas(root_frame, width=25, height=200, highlightthickness=0)
sidebar.grid(row=0, column=1)
button_filter = Button(sidebar, image=filter_icon, command=filter_setting, bd=0, highlightthickness=0)
button_add = Button(sidebar, image=add_icon, command=lambda: add(), bd=0, )
button_volume_state = Button(sidebar, image=volume_state_icon, command=change_volume_state, bd=0)
button_delete_bin = Button(sidebar, image=delete_bin_icon, command=delete_all, bd=0)
sidebar.create_window(10, 15, window=button_add)
sidebar.create_window(10, 40, window=button_filter)
sidebar.create_window(14, 65, window=button_volume_state)
sidebar.create_window(10, 95, window=button_delete_bin)

# background setup
window2 = Toplevel()
window2.overrideredirect(True)
window2.attributes("-topmost", True)
bg_canvas = Canvas(window2, width=600, height=200, highlightthickness=0, bd=0)
bg_canvas.grid(row=0, column=0)
bg_canvas.create_image(300, 95, image=file)
window2.bind('<FocusIn>', focus_handling)
root.bind("<FocusIn>", focus_handling)
root.bind("<Configure>", force_background)
sidebar.bind("<Unmap>", minimize_bg)
root.bind("<Map>", unminimize_bg)

# capturing exit from the app to save data just in time before exit
root.protocol("WM_DELETE_WINDOW", save)
load()

# launching the main processes
count()
root.mainloop()

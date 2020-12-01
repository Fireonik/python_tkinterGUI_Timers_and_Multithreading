from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from copy import deepcopy
from playsound import playsound
from PIL import ImageTk
import threading
import math
import time


class Timer:
    def __init__(self):
        self.interval = 0
        self.signal = 'Auratone'
        self.label = []
        self.label_text = StringVar()
        self.type = ''
        self.time_point = {}


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


@thread
def count():
    def one_thread_is_enough():
        global timers, timer_list, timer_was_deleted, bodoni26

        def timer_ticking(ind):
            try:
                timers[ind].interval -= 1
                timers[ind].label_text.set(interval_formatted(ind))
                if timers[ind].interval == 0:
                    sound_thread(timers[ind].signal + ".mp3")
                    message_thread()
                    timers[ind].label[0].destroy()
                    del timers[ind]
                    return True
                return False
            except IndexError:
                pass
        size = len(timers)
        timer_list.config(scrollregion=(0, 0, 265, 100+40*size))
        if size > 0:
            for i in range(size):
                if timer_ticking(i):
                    timer_was_deleted = True
        if timer_was_deleted:
            for i in range(len(timers)):
                timers[i].label[0].destroy()
                del timers[i].label[0]
                temp_label = Label(timer_list, textvariable=timers[i].label_text, font=bodoni26, foreground='#622651')
                timers[i].label.append(temp_label)
                timer_list.create_window(260, 40 * i, window=timers[i].label[0], anchor='ne')
                timer_was_deleted = False
        del size
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
    root.deiconify()  # WTF


def force_background(event=None):
    global window2, root
    x = deepcopy(str(root.winfo_rootx()))
    y = deepcopy(str(root.winfo_rooty()))
    window2.geometry('290x200' + '+' + x + '+' + y)
    del x, y


def scroll_timer_list(event):
    timer_list.yview_scroll(int(event.delta / 120), "units")


def timer_setup():
    def confirm_add(event=None):
        interval = eval(days.get())*86400 + eval(hours.get())*3600 + eval(minutes.get())*60 + eval(seconds.get())
        if interval <= 0:
            messagebox.showwarning(title='NERV', message='Invalid interval')
            return
        timers.append(Timer())
        timers[-1].type = 'Timer'
        timers[-1].interval = interval
        timers[-1].signal = signal.get()
        timers[-1].label_text.set(interval_formatted(-1))
        timers[-1].label.append(Label(timer_list, textvariable=timers[-1].label_text, font=bodoni26, foreground='#622651'))
        timer_list.create_window(260, 40 * (len(timers) - 1), window=timers[-1].label[0], anchor='ne')
        timer_setup_window.destroy()

    timer_setup_window = Toplevel()
    timer_setup_window.attributes("-topmost", True)
    timer_setup_window.geometry('435x58' + '+' + str(root.winfo_rootx() + 50) + '+' + str(root.winfo_rooty() + 50))
    bodoni14 = font.Font(family="Bodoni MT", size=14)
    days = Spinbox(timer_setup_window, from_=0, to=365, width=3, font=bodoni14, state='readonly', foreground='#622651')
    days.grid(row=1, column=0, padx=1)
    hours = Spinbox(timer_setup_window, from_=0, to=23, width=2, font=bodoni14, state='readonly', foreground='#622651')
    hours.grid(row=1, column=1)
    minutes = Spinbox(timer_setup_window, from_=0, to=59, width=2, font=bodoni14, state='readonly', foreground='#622651')
    minutes.grid(row=1, column=2)
    seconds = Spinbox(timer_setup_window, from_=0, to=59, width=2, font=bodoni14, state='readonly', foreground='#622651')
    seconds.grid(row=1, column=3)
    signal = Spinbox(timer_setup_window, values=("Auratone", "Softchime", "Happyday", "Ping1", "Ping2"), font=bodoni14, state='readonly', foreground='#622651')
    signal.grid(row=1, column=4)
    Button(timer_setup_window, command=confirm_add, text="OK", font=font.Font(family='Bodoni MT', size=16)).grid(row=0, column=5, rowspan=2, columnspan=2, ipady=6, padx=3, ipadx=15)
    Label(timer_setup_window, text='ddd', font=bodoni14, foreground='#622651').grid(row=0, column=0, sticky='w')
    Label(timer_setup_window, text='hh', font=bodoni14, foreground='#622651').grid(row=0, column=1, sticky='w')
    Label(timer_setup_window, text='mm', font=bodoni14, foreground='#622651').grid(row=0, column=2, sticky='w')
    Label(timer_setup_window, text='ss', font=bodoni14, foreground='#622651').grid(row=0, column=3, sticky='w')
    Label(timer_setup_window, text='signal', font=bodoni14, foreground='#622651').grid(row=0, column=4, sticky='w')


def time_point_formatted(mon, d, h, minute, s):
    a = [mon, d, h, minute, s]
    for ind in range(5):
        if int(a[ind]) < 10:
            a[ind] = '0' + a[ind]
    return a[0] + '.' + a[1] + ' ' + a[2] + ":" + a[3] + ':' + a[4]


def alarm_setup():
    def confirm_add(event=None):
        m = int(month.get())
        d = int(day.get())
        if m in {4, 6, 9, 11} and d == 31 or m == 2 and d > 29:
            messagebox.showwarning(title='NERV', message='Invalid day number')
            return
        timers.append(Timer())
        timers[-1].type = 'Alarm'
        timers[-1].time_point['month'] = int(month.get())
        timers[-1].time_point['day'] = int(day.get())
        timers[-1].time_point['hour'] = int(hour.get())
        timers[-1].time_point['minute'] = int(minute.get())
        timers[-1].time_point['second'] = int(second.get())
        timers[-1].signal = signal.get()
        timers[-1].label_text.set(time_point_formatted(month.get(), day.get(), hour.get(), minute.get(), second.get()))
        timers[-1].label.append(Label(timer_list, textvariable=timers[-1].label_text, font=bodoni26, foreground='#622651'))
        timer_list.create_window(260, 40 * (len(timers)-1), window=timers[-1].label[0], anchor='ne')
        nonlocal alarm_setup_window
        alarm_setup_window.destroy()

    alarm_setup_window = Toplevel()
    alarm_setup_window.attributes("-topmost", True)
    alarm_setup_window.geometry('480x60' + '+' + str(root.winfo_rootx() + 50) + '+' + str(root.winfo_rooty() + 50))
    bodoni14 = font.Font(family="Bodoni MT", size=14)
    Label(alarm_setup_window, text='mon', font=bodoni14, foreground='#622651').grid(row=0, column=0)
    Label(alarm_setup_window, text='day', font=bodoni14, foreground='#622651').grid(row=0, column=1)
    Label(alarm_setup_window, text='hour', font=bodoni14, foreground='#622651').grid(row=0, column=2)
    Label(alarm_setup_window, text='min', font=bodoni14, foreground='#622651').grid(row=0, column=3)
    Label(alarm_setup_window, text='sec', font=bodoni14, foreground='#622651').grid(row=0, column=4)
    Label(alarm_setup_window, text='signal', font=bodoni14, foreground='#622651').grid(row=0, column=5, sticky='w')
    month = Spinbox(alarm_setup_window, from_=1, to=12, width=2, font=bodoni14, state='readonly', foreground='#622651')
    month.grid(row=1, column=0)
    day = Spinbox(alarm_setup_window, from_=1, to=31, width=2, font=bodoni14, state='readonly', foreground='#622651')
    day.grid(row=1, column=1)
    hour = Spinbox(alarm_setup_window, from_=0, to=23, width=2, font=bodoni14, state='readonly', foreground='#622651')
    hour.grid(row=1, column=2)
    minute = Spinbox(alarm_setup_window, from_=0, to=59, width=2, font=bodoni14, state='readonly', foreground='#622651')
    minute.grid(row=1, column=3)
    second = Spinbox(alarm_setup_window, from_=0, to=59, width=2, font=bodoni14, state='readonly', foreground='#622651')
    second.grid(row=1, column=4)
    signal = Spinbox(alarm_setup_window, values=("Auratone", "Softchime", "Happyday", "Ping1", "Ping2"), font=bodoni14, state='readonly', foreground='#622651')
    signal.grid(row=1, column=5)
    Button(alarm_setup_window, command=confirm_add, text="OK", font=font.Font(family='Bodoni MT', size=16)).grid(row=0, ipady=4,column=6, rowspan=2, columnspan=2, sticky='s', padx=5, ipadx=15)


def add():
    def move_to_timer_setup(event=None):
        timer_setup_window.destroy()
        timer_setup()

    def move_to_alarm_setup(event=None):
        timer_setup_window.destroy()
        alarm_setup()

    timer_setup_window = Toplevel()
    timer_setup_window.attributes("-topmost", True)
    timer_setup_window.geometry('169x39' + '+' + str(root.winfo_rootx()+60) + '+' + str(root.winfo_rooty()+50))
    Button(timer_setup_window, text="Timer", command=move_to_timer_setup, font=font.Font(family='Bodoni MT', size=14), foreground='#622651').grid(row=0, column=0, ipadx=10)
    Button(timer_setup_window, text="Alarm", command=move_to_alarm_setup, font=font.Font(family='Bodoni MT', size=14), foreground='#622651').grid(row=0, column=1, ipadx=10)


root = Tk()

# global variables
timers = []
timer_was_deleted = False
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
scroll_y = Scrollbar(timer_list, orient="vertical", command=timer_list.yview)
timer_list.grid(row=0, column=0, sticky=(N, W, E, S))
timer_list.configure(yscrollcommand=scroll_y.set)
timer_list.bind_all("<MouseWheel>", scroll_timer_list)
sidebar = Canvas(root_frame, width=25, height=200, highlightthickness=0)
sidebar.grid(row=0, column=1)
button_settings = Button(sidebar, image=settings, bd=0, highlightthickness=0)
button_add = Button(sidebar, image=add_icon, command=lambda: add(), bd=0, )
sidebar.create_window(10, 15, window=button_settings)
sidebar.create_window(10, 40, window=button_add)

# background setup
window2 = Toplevel()
window2.overrideredirect(True)
window2.attributes("-topmost", True)
bg_frame = Frame(window2)
bg_frame.grid()
bg_canvas = Canvas(bg_frame, width=290, height=200, highlightthickness=0, bd=0)
bg_canvas.grid(row=0, column=0, sticky='nw')
bg_canvas.create_image(140, 95, image=file)
window2.bind('<FocusIn>', focus_handling)
root.bind("<FocusIn>", focus_handling)
root.bind("<Configure>", force_background)
sidebar.bind("<Unmap>", minimize_bg)
root.bind("<Map>", unminimize_bg)

count()
root.mainloop()

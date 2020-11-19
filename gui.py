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
    txt1.set(a[0])
    root.after(1000, count, txt1, a)


root = Tk()
root.title("NERV")
root.grid()
canvas = Canvas(root, width=800, height=600, scrollregion=(0, 0, 800, 1200), background='black')
canvas.grid(row=0, column=0)

scroll_x = Scrollbar(canvas, orient="horizontal", command=canvas.xview)

scroll_y = Scrollbar(canvas, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)


def on_mousewheel(event):
    canvas.yview_scroll(int(event.delta/120), "units")

canvas.bind_all("<MouseWheel>", on_mousewheel)


A = ['10000000000']

text1 = StringVar()
text1.set(A[0])
century65 = font.Font(family="Century", name="Century65", size=65)
label = ttk.Label(canvas, textvariable=text1, font=century65, background='black', foreground='white')
canvas.create_window(300, 60, window=label)

timer_settings = PhotoImage(file="clock_settings50px.gif")
button_timer_settings = Button(canvas, image=timer_settings, bg="black")
canvas.create_window(600, 65, window=button_timer_settings)

settings = PhotoImage(file="settings50px.gif")
button_settings = Button(canvas, image=settings, bg="black")
canvas.create_window(725, 65, window=button_settings)

filter_icon = PhotoImage(file="filter50px.gif")
button_filter = Button(canvas, image=filter_icon, bg="black")
canvas.create_window(725, 125, window=button_filter)

button = Button(canvas, text="1234")
canvas.create_window(400, 1100, window=button)
count(text1, A)
root.mainloop()

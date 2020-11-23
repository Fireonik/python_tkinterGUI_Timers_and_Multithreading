from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from copy import deepcopy
from playsound import playsound
import threading

root = Tk()
frame = Frame(root)
frame.grid()
canvas = Canvas(root, width=500, height=1000)
canvas.grid()

a = []
aa = []
for i in range(10):
    bb = StringVar()
    bb.set("123")
    aa.append(bb)
    b = ttk.Label(canvas, textvariable=aa[i])
    a.append(b)
    canvas.create_window(100, 80*(i+1), window=b)
aa[5].set("ORA ORA ORA")
mainloop()

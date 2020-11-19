from tkinter import *
from tkinter import ttk
from tkinter import font

root = Tk()
root.title("NERV")
canvas = Canvas(root, width=1000, height=660, background='black')
canvas.grid()

CenturyFont70 = font.Font(family='Century', name='CenturyFont70', size=70, weight='bold')
CenturyFont90 = font.Font(family='Century', name='CenturyFont90', size=90, weight='bold')
Helvetica50 = font.Font(family='Helvetica', name='Helvetica50', size=50, weight='bold')
Helvetica70 = font.Font(family='Helvetica', name='Helvetica70', size=70, weight='bold')

line1 = ttk.Label(canvas, text='NEON', font=CenturyFont70, foreground='white', background='black')
line2 = ttk.Label(canvas, text='GENESIS', font=CenturyFont70, foreground='white', background='black')
line3 = ttk.Label(canvas, text='EVANGELION', font=CenturyFont90, foreground='white', background='black')
line4 = ttk.Label(canvas, text='EPISODE:8', font=Helvetica50, foreground='white', background='black')
line5 = ttk.Label(canvas, text='ASUKA STRIKES!', font=Helvetica70, foreground='white', background='black')

canvas.create_window(200, 100, window=line1)
canvas.create_window(275, 200, window=line2)
canvas.create_window(480, 320, window=line3)
canvas.create_window(230, 475, window=line4)
canvas.create_window(575, 560, window=line5)

root.resizable(False, False)
root.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import font

root = Tk()
root.title("Briefing Manager")
canvas = Canvas(root, width=1050, height=580)
canvas.grid()

BodoniMT250 = font.Font(family='Bodoni MT', name='BodoniMT250', size=250)
BodoniMT50 = font.Font(family='Bodoni MT', name='BodoniMT50', size=50)
BodoniMT75 = font.Font(family='Bodoni MT', name='BodoniMT75', size=75)

line1 = ttk.Label(canvas, text='Alive', font=BodoniMT250)
line2 = ttk.Label(canvas, text='Angel Beats!', font=BodoniMT50)
line3 = ttk.Label(canvas, text='EPISODE.07', font=BodoniMT75)

canvas.create_window(470, 200, window=line1)
canvas.create_window(575, 375, window=line2)
canvas.create_window(675, 475, window=line3)

root.resizable(False, False)
root.mainloop()

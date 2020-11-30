learning process of the python tkinterGUI and other topics needed to develop timers app

nov 17:    I'm done trying to learn pyqt, switching to tkinter, created repository

nov 18:    practiced using simplest widgets, fonts, colors, and canvas widget in particular; 
           learned how to place widgets onto the canvas, build .EXE with custom icon, 
           built my first graphic and first .exe app NERV.exe
        
nov 19:    learned how to make buttons with custom icons to keep GUI nice and simple, 
           and how to modificate icons in paint.NET, how to make tkinter canvas scrollable, 
           learned basics on parallel threads, learned about @decorators in python

nov 20:    learned about creating windows separate from main in tkinter, how to change 
           contents of the current window, how to remove borders of the buttons, how to
           create combobox and set a default value to it, done some designing work on 
           the timer system, also learned about extensions system in pycharm and tried
           deep code AI

nov 20-23: developed core features of the timers: timers can be added with a custom interval, 
           there are 5 signals to choose from, timer quantity is not limited,  the list 
           of timers can be seen as an abyssal scroll, each interval is displayed there,
           displaying remaining time as it ticks; visual style of the app went through
           redesign, now the app is very compact and light-looking. Most importantly,
           timers work, and their ticking and signal displaying are handled with separate
           threads so that time does not stop ticking while UI is used;  
           Also since i want my app to look nice, (anything consisting of comboboxes on 
           white background is ugly, basically) i developed idea on how to implement 
           background in tkinter

nov 25-26: implemented background, learned some design basics like using color palettes, 
           tweaked icons, changed font, implemented conversion of the time interval in
           seconds into time format, encountered memory leaks, reworked multithreading
           to eliminate all leaks (yet still didnt figure out how looped creation-destruction
           of the thread causes it), cleaned up the code a bit, added a few comments, fixed
           a few problems in the code

nov 30:    strange bug already wasted abyss of time and looks like it is going to waste another

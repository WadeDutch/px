import tkinter as tk
from application import App

#init window
master = tk.Tk()
master.state("zoomed")
App(master)
master.mainloop()

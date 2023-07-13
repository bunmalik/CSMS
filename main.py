#! /usr/bin/python3

from tkinter import *
from forms import login
import models

models.create_tables_if_not_exist()
root=Tk()
root.resizable(True,True)
log=login.Login(root)
root.mainloop()

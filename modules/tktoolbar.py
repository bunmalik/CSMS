#tb.py

from tkinter import *
from tkinter import ttk
from models import Users as User

def _init_toolbar(tbmaster):

    '''TOOLBAR CONTAINS ADD, EDIT, DELETE AND FIND BUTTONS
        the argment is a class and it must have:
        tbmaster.frame              :- a root window class
        tbmaster.btn_add_click()    :- a method
        tbmaster.btn_edit_click()
        tbmaster.btn_delete_click()
        tbmaster.btn_find_click()
        '''
    tbmaster.tb=Frame(tbmaster.frame,borderwidth=1)#,relief=)
    tbmaster.tb.pack(side=TOP,fill=X)#####
    imgdir="images/16x16/"
    tbmaster.btn_add=Button(tbmaster.tb,text = "Add +",bg="green",fg="white",font=("Calibri", 15,'underline italic'),command=tbmaster.btn_add_click)
    # tbmaster.imgadd=PhotoImage(file=imgdir+"add.gif")
    # tbmaster.btn_add['image']=tbmaster.imgadd
    tbmaster.btn_add.pack(side=LEFT,padx=4,pady=4)

    tbmaster.btn_edit=Button(tbmaster.tb,text = "Edit /", bg="green",fg="white",font=("Calibri", 15),command=tbmaster.btn_edit_click)
    # tbmaster.imgedit=PhotoImage(file=imgdir+"edit2.gif")
    # tbmaster.btn_edit['image']=tbmaster.imgedit
    tbmaster.btn_edit.pack(side=LEFT,padx=4,pady=4)

    tbmaster.btn_delete=Button(tbmaster.tb,text = "Delete -",bg="red",fg="white",font=("Calibri", 15),command=tbmaster.btn_del_click)
    # tbmaster.imgdel=PhotoImage(file=imgdir+"delete.gif")
    # tbmaster.btn_delete['image']=tbmaster.imgdel
    tbmaster.btn_delete.pack(side=LEFT,padx=4,pady=4)

    tbmaster.btn_find=Label(tbmaster.tb,text = "Search @",bg="green",fg="white",font=("Calibri", 15))
    # tbmaster.imgfind=PhotoImage(file=imgdir+"find.gif")
    # tbmaster.btn_find['image']=tbmaster.imgfind
    tbmaster.btn_find.pack(side=LEFT,padx=4,pady=4)

    tbmaster.tb_entryfind=Entry(tbmaster.tb)
    tbmaster.tb_entryfind.pack(side=LEFT,padx=4,pady=4)


    staffs = []; admins = []
    adminss = User.select().where(User.is_admin.contains("yes"))
    staffss = User.select().where(User.is_admin.contains("no"))

    myfile=open("Staff","r")
    staffname = myfile.read().splitlines()

    for user in adminss: admins.append(user.username)
    for user in staffss: staffs.append(user.username)
##    print(admins)
##    print(staffs)
##    if staffname not in admins:
##        tbmaster.btn_delete.configure(state="disabled")
##    else:
##        tbmaster.btn_delete.configure(state="active")

def _init_stafftoolbar(tbmaster):

    '''THIS TOOLBAR CONTAINS OPEN, DELETE AND SEACH FIELD
        the argment is a class and it must have:
        tbmaster.frame              :- a root window class
        tbmaster.btn_edit_click()
        tbmaster.btn_delete_click()
        tbmaster.btn_find_click()
        '''
    tbmaster.tb=Frame(tbmaster.frame,borderwidth=1)#,relief=)
    tbmaster.tb.pack(side=TOP,fill=X)#####
    imgdir="images/16x16/"

    tbmaster.btn_edit=Button(tbmaster.tb,text = "Open", bg="green",fg="white",font=("Calibri", 15),command=tbmaster.btn_edit_click)
    # tbmaster.imgedit=PhotoImage(file=imgdir+"edit2.gif")
    # tbmaster.btn_edit['image']=tbmaster.imgedit
    tbmaster.btn_edit.pack(side=LEFT,padx=4,pady=4)

    tbmaster.btn_delete=Button(tbmaster.tb,text = "Delete -",bg="red",fg="white",font=("Calibri", 15),command=tbmaster.btn_del_click)
    # tbmaster.imgdel=PhotoImage(file=imgdir+"delete.gif")
    # tbmaster.btn_delete['image']=tbmaster.imgdel
    tbmaster.btn_delete.pack(side=LEFT,padx=4,pady=4)

    tbmaster.btn_find=Label(tbmaster.tb,text = "Search @",bg="green",fg="white",font=("Calibri", 15))
    # tbmaster.imgfind=PhotoImage(file=imgdir+"find.gif")
    # tbmaster.btn_find['image']=tbmaster.imgfind
    tbmaster.btn_find.pack(side=LEFT,padx=4,pady=4)

    tbmaster.tb_entryfind=Entry(tbmaster.tb)
    tbmaster.tb_entryfind.pack(side=LEFT,padx=4,pady=4)

from tkinter import *
from tkinter import ttk
from modules.tkcalendar import ttkCalendar
from forms import staffs, products, invoices, addinvoice
from forms.invoices import FormInvoices
from forms.addinvoice import FormAddInvoice
from tkinter.messagebox import showinfo, showerror
from models import Users as User
from werkzeug.security import check_password_hash


import sys
import time
sys.dont_write_bytecode = True

class FormMenu:
    """This is the main form that shows after user login.
    Contains
    =========
    --> Label shows login Company name.
    --> Three Buttons
        --> Products:   OnClick Shows FormProducts,
        --> Invoices:   OnClick Shows FormInvoices,
        --> Customers:  OnClick shows FormCustomers
        --> Management:
    --> A background Image


    Features:
    - Add as many products as you like to the database.
    - Update products as per your choice
    - Handle Dynamic sales.
    - Mathmatically accurate sales.
    - Generate Bill, Save as well as print it.
    - Notifies less stock in the database.
    - Compiled so that it can be run on any windows platfrom without having to install Python.
    - Notifies shop onwer the sales made in the shop
    - Has admin and staff login
    - Maximum login attempts is four
    - Database contains product, staff and invoice tables
    - Verifies Only shop owner's contact
    """
    def __init__(self):
        self.frame=Toplevel()
        self.frame.title("ComStore Pro")
        self.frame['bg']='blue'
        self.frame.resizable(True,True)
        self.frame.wm_attributes('-fullscreen', True)
        #self.frame.geometry("1000x1000+0+500")

        self.frm_invoices=None
        self.frm_calendar=None
        self.frame.bind("<KeyPress>",self.close_form)

        self._init_menu()
        self._init_widgets()

    def _init_menu(self):
        #self.frame.bind("<KeyPress>", lambda e: self.keypressed(e))

        #lambda x: x*10 if x<2 else (x**2 if x<4 else x+10)

        self.menu = Menu(self.frame)
        self.frame.config(menu=self.menu)
        filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Products...", command=self.admin_manage_products)
        filemenu.add_command(label="Invoices...", command=self.invoices_click)
        filemenu.add_command(label="Create Invoice...", command=self.addinvoice_click)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.frame.destroy)
        helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About...", command=self.about_click)

    def about_click(self):
        w=Toplevel()
        lbl1=Label(w,text="Welcome to ComStore Pro. version 1.0\nDesigned by \nJoseph K. Anane and Dacosta Gyamfi")
        lbl1.pack(side="top",padx=10,pady=10)
        lbl3=Label(w,text="for help contact me at: \n0246746622\0242518872\nEmail:biganane@gmail.com\nfocustony50@gmail.com")
        lbl3.pack(side="top",padx=10,pady=10)
        lbl3=Label(w,text="Credit: Anas Musah \nbunmalik11@gmail.com")
        lbl3.pack(side="top",padx=10,pady=10)

    def _init_widgets(self):
        #initiate toolbar

        style1 = ttk.Style()
        style1.configure("My.TFrame", foreground="white", background="blue")
        self.toolbar = ttk.Frame(self.frame,style="My.TFrame")
        imgdir="images/24x24/"
        # self.toolbar.imghome=PhotoImage(file=imgdir+"home.gif")
        # self.toolbar.imgcalc=PhotoImage(file=imgdir+"calc.gif")
        # self.toolbar.imgcalander=PhotoImage(file=imgdir+"date.gif")
        # self.toolbar.imgexit=PhotoImage(file=imgdir+"exit.gif")
        # self.toolbar.imghelp=PhotoImage(file=imgdir+"help.gif")
        butcompany=Button(self.toolbar,text="Home",bg="green",font=("Calibri", 15),height=2, width=7)
        butcompany.pack(side=LEFT,padx=2)
        #lbl0=Label(self.toolbar,text='ComStore Pro').pack(side=LEFT,padx=5)

        butcalc=Button(self.toolbar,text="Calculator",font=("Calibri", 15),command=self.calc_click,height=2, width=9)
        butcalc.pack(side=LEFT,padx=2)
        butcalendar=Button(self.toolbar,text = "Calender",font=("Calibri", 15),command=self.calendar_click,height=2, width=8)
        butcalendar.pack(side=LEFT,padx=2)

        butexit=Button(self.toolbar,text="Exit",font=("Calibri", 15),command=self.frame.destroy,height=2, width=7)
        butexit.pack(side=RIGHT,padx=2)
        buthelp=Button(self.toolbar,text = "About",font=("Calibri", 15),command=self.about_click,height=2, width=7)
        buthelp.pack(side=RIGHT,padx=2)
        self.toolbar.pack(side='top',fill='x')

        Label(self.frame,text='  ')

        style2 = ttk.Style()
        style2.configure("BW.TLabel", foreground="yellow", background="green")
        self.frames = ttk.Frame(self.frame, style="BW.TLabel")
        myfile=open("Staff","r")
        self.staffname = myfile.read().splitlines()
        lbl_welcome=ttk.Label(self.frames,style="BW.TLabel",text="Staff:"+" "+self.staffname[0], font=("Calibri", 20))
        lbl_welcome.pack(side=RIGHT,padx = 20,pady=4)
        global clock
        clock = ttk.Label(self.frames, text = '', style="BW.TLabel",font=("Calibri", 20) )
        clock.pack(side=LEFT, anchor = E,padx=20)
        self.tick()
        self.frames.pack(side=TOP, fill=X)


        #buttons frame
        #--------------------------------------------
        style3 = ttk.Style()
        style3.configure("My.TLabel", foreground="white", background="green")
        self.buttons = ttk.Frame(self.frame, style="My.TLabel")

        #button products
        self.labelframe = Label(self.buttons, text="Tasks", font=("Calibri", 15))
        self.labelframe.pack(side='top',anchor=W)
        lbl0=ttk.Label(self.buttons,text="-"*45, style="My.TLabel").pack()

        self.btnproducts = Button(self.buttons,text = "Products...",font=("Calibri", 15) ,height=1, width=18,command=self.admin_manage_products)
        # self.imgprdt=PhotoImage(file="images/products.gif")#self.btnproducts['font']=("Helvetica", 16)
        # self.btnproducts['image']=self.imgprdt
        self.btnproducts.pack(side='top')#, fill='x')
        lbl1=ttk.Label(self.buttons,text=" ", style="My.TLabel").pack()

        #button invoices
        self.btninvoices = Button(self.buttons,text = "Invoices...",font=("Calibri", 15),height=1, width=18,command=self.invoices_click)
        # self.imginv=PhotoImage(file="images/invoices.gif")
        # self.btninvoices['image']=self.imginv
        self.btninvoices.pack(side='top')
        lbl2=ttk.Label(self.buttons,text=" ", style="My.TLabel").pack()

        #button customers
        self.btncustomers = Button(self.buttons, text="Create Invoice.." ,font=("Calibri", 15),height=1, width=18,command=self.addinvoice_click)
        # self.imgcust=PhotoImage(file="images/customers.gif")
        # self.btncustomers['image']=self.imgcust
        self.btncustomers.pack(side='top')
        lbl3=ttk.Label(self.buttons,text=" ", style="My.TLabel").pack()
        self.buttons.pack(side='right', padx=10)

        #button customers
        self.btnstaffs = Button(self.buttons, text="Manage staffs ..." ,font=("Calibri", 15),height=1, width=18,command=self.admin_manage_staffs)
        # self.imgcust=PhotoImage(file="images/customers.gif")
        # self.btncustomers['image']=self.imgcust
        self.btnstaffs.pack(side='top')
        lbl3=ttk.Label(self.buttons,text=" ", style="My.TLabel").pack()
        self.buttons.pack(side='right',padx=10,pady=1)

        # self.frame5 = ttk.Frame(self.frame)
        # lbl_produt_help=ttk.Label(self.frame5,style="BW.TLabel",text="""Press <p> to open products' window.\nPress <i> to open inventory window.\nPress <c> to create an inventory.""",font=("Calibri", 15))
        # lbl_produt_help.pack(side=LEFT)
        # self.frame5.pack(side="bottom",anchor=W, padx=15,pady=15)

        #background label
        #-------------------------------------------
        # self.imgback=PhotoImage(file="images/back.gif")
        # self.lblbackground= Label(self.frame, style="BW.TLabel",borderwidth=0)
        # self.lblbackground.pack()
        #self.lblbackground['image'] = self.imgback

    def close_form(self,event):
        if event.keycode ==27:
            self.frame.quit()

    def calc_click(self):
        import os
        try: os.startfile('calc.exe')
        except: showinfo("info", "Calculator doesn't exist!",icon='info')

    #calendar-------
    def calendar_click(self):
        if self.frm_calendar==None:
            self.frm_calendar=ttkCalendar(master=self.frame)
        elif self.frm_calendar.flag: #frm_products currently opened
            #print ('already a window exists')
            showinfo("Info", "Calender has been opened already!",parent=self.frame)
            return 0
        else:
            self.frm_calendar=ttkCalendar(master=self.frame)

        self.frame.wait_window(self.frm_calendar.top)
        #print (self.frm_calendar.datepicked)

    # time ...
    def tick(self):
        from datetime import datetime
        curtime=''
        newtime = time.strftime('%H:%M:%S')
        if newtime != curtime:
            curtime =  datetime.today().strftime("%A")+", "+str(datetime.today())[:10]+ "\n"+ newtime
            clock.config(text=curtime)
        clock.after(200, self.tick)


    def keypressed(self,event):
        #33 p, 31 i, 54 c, escape 27
        if sys.platform == 'linux':
            if event.keycode == 33: self.products_click()
            elif event.keycode == 31: self.invoices_click()
            elif event.keycode == 54: self.addinvoice_click()
            elif event.keycode ==27: self.frame.destroy()
        elif sys.platform == 'win32':
            if event.keycode == 112: self.products_click()
            elif event.keycode == 105: self.invoices_click()
            elif event.keycode == 99: self.addinvoice_click()
            elif event.keycode == 27: self.frame.destroy()

    def products_click(self):
        #print ("products")
        #self.frame.withdraw()

        pwd = admin_pwd_entry.get()
        passwords = []; admin = []
        staffss = User.select().where(User.is_admin.contains("yes"))


        for user in staffss:
            passwords.append(user.password)
            admin.append(user.username)
        

        if pwd == '':
            showerror("Error","Password required",parent=admin_login_screen)
        else:
            if any(self.staffname[0] == admin[i] and check_password_hash(passwords[i],pwd)==True for i in range(0,len(passwords))):
                showinfo("Bravo", "Access granted",parent=admin_login_screen)
                admin_login_screen.destroy()
                self.frm_products=products.FormProducts()
                self.frame.wait_window(self.frm_products.frame)
                self.frame.deiconify()
            else:
                showerror("Sorry", "Access denied!\nOnly for admin",parent=admin_login_screen)

    def invoices_click(self):
        #print ("invoices")
        #self.frame.withdraw()
        self.frm_invoices=invoices.FormInvoices()
        self.frame.wait_window(self.frm_invoices.frame)
        self.frame.deiconify()

    def addinvoice_click(self):
        #print ("add_invoice")
        #self.frame.withdraw()
        self.frm_invoices=addinvoice.FormAddInvoice()
        self.frame.wait_window(self.frm_invoices.frame)
        self.frame.deiconify()

    def manage_staffs_click(self):
        pwd = admin_pwd_entry.get()
        passwords = []; admin = []
        staffss = User.select().where(User.is_admin.contains("yes"))

        for user in staffss:
            passwords.append(user.password)
            admin.append(user.username)
        print(admin)
        print(passwords)
        print(self.staffname)
        if pwd == '':
            showerror("Error","Password required",parent=admin_login_screen)
        else:

            if any(self.staffname[0] == admin[i] and check_password_hash(passwords[i],pwd)==True for i in range(0,len(passwords))):
                showinfo("Bravo", "Access granted",parent=admin_login_screen)
                admin_login_screen.destroy()
                self.staff=staffs.FormUsers()
                #self.frame.wait_window(self.staff.frame)
            else:
                showerror("Sorry", "Access denied!\nOnly for admins",parent=admin_login_screen)

    def admin_manage_staffs(self):
        global admin_login_screen
        global admin_login_entry
        global admin_pwd_entry
        global butstaffs
        global butproducts
        admin_verify = StringVar()
        admin_pwd_verify = StringVar()

        admin_login_screen = Toplevel(self.frame)
        admin_login_screen.title("Admin Login")
        admin_login_screen.geometry("300x200+500+300")
        admin_login_screen.wm_attributes("-top", 1)
        admin_login_screen.grab_set()
        admin_login_screen.resizable(0,0)
        admin_login_screen.wm_attributes('-fullscreen', False)
        Label( admin_login_screen, text="Password * ").pack()
        admin_pwd_entry = Entry( admin_login_screen, textvariable=admin_pwd_verify, show= '*')
        admin_pwd_entry.pack()
        admin_pwd_entry.focus_set()
        Label( admin_login_screen, text="").pack()
        butstaffs = Button( admin_login_screen, text="Login", width=12, height=1, bg="blue",fg="white",font=("Calibri", 13),command = self.manage_staffs_click)
        butstaffs.pack()
        Label(admin_login_screen, text="").pack()
        butforgotpassword = Button( admin_login_screen, text="forgot password?", width=13, height=1,font=("Calibri", 11),command = self.forgotpassword_keypress)
        butforgotpassword.pack()
        butforgotpassword.bind("<KeyPress>",self.forgotpassword_keypress)
        butcancel = Button( admin_login_screen,text="Cancel", height="1", width="12", bg="orange" ,command=admin_login_screen.destroy)
        butcancel.pack(side='bottom')
        butcancel.bind("<KeyPress>",self.cancel_keypress)
        admin_login_screen.bind("<KeyPress>", self.admin_manage_staffs_keypress)

    def admin_manage_products(self):
        global admin_login_screen
        global admin_login_entry
        global admin_pwd_entry
        global butstaffs
        global butproducts
        admin_verify = StringVar()
        admin_pwd_verify = StringVar()

        admin_login_screen = Toplevel(self.frame)
        admin_login_screen.title("Admin Login")
        admin_login_screen.geometry("300x200+500+300")
        admin_login_screen.wm_attributes("-top", 1)
        admin_login_screen.grab_set()
        admin_login_screen.resizable(0,0)
        admin_login_screen.wm_attributes('-fullscreen', False)
        Label( admin_login_screen, text="Password * ").pack()
        admin_pwd_entry = Entry( admin_login_screen, textvariable=admin_pwd_verify, show= '*')
        admin_pwd_entry.pack()
        admin_pwd_entry.focus_set()
        Label( admin_login_screen, text="").pack()
        butstaffs = Button( admin_login_screen, text="Login", width=12, height=1, bg="blue",fg="white",font=("Calibri", 13),command = self.products_click)
        butstaffs.pack()
        Label(admin_login_screen, text="").pack()
        butforgotpassword = Button( admin_login_screen, text="forgot password?", width=13, height=1,font=("Calibri", 11),command = self.forgotpassword_keypress)
        butforgotpassword.pack()
        butforgotpassword.bind("<KeyPress>",self.forgotpassword_keypress)
        butcancel = Button( admin_login_screen,text="Cancel", height="1", width="12", bg="orange" ,command=admin_login_screen.destroy)
        butcancel.pack(side='bottom')
        butcancel.bind("<KeyPress>",self.cancel_keypress)
        admin_login_screen.bind("<KeyPress>", self.admin_manage_products_keypress)

    def forgotpassword_keypress(self):
        showinfo("Info","Kindly quit and restart to change your password",parent=admin_login_screen)

    def butlogin_keypress(self,event):
        if event.keycode ==27:
            self.manage_staffs_click()

    def admin_manage_staffs_keypress(self,event):
        if event.keycode ==13:
            self.manage_staffs_click()
        elif event.keycode ==27:
            admin_login_screen.destroy()
    def admin_manage_products_keypress(self,event):
        if event.keycode ==13:
            self.products_click()
        elif event.keycode ==27:
            admin_login_screen.destroy()

    def cancel_keypress(self,event):
        if event.keycode ==13:
            admin_login_screen.destroy()

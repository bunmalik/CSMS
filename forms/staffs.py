from tkinter import *
from tkinter import ttk
from modules.tklistview import MultiListbox
from modules.tktoolbar import _init_toolbar,_init_stafftoolbar
#from models import Inventory_User as User
from models import Users as User
from tkinter.messagebox import showinfo
from tkinter import messagebox
from werkzeug.security import generate_password_hash, check_password_hash

import nexmo
import random as rand
client = nexmo.Client(key='e9d6bfb6', secret='OUJ8GmGwPRQmnAQ4')

import string
def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(rand.choice(lettersAndDigits) for i in range(stringLength))



class FormUsers:
    '''The Users window with toolbar and a datagrid of Users'''
    def __init__(self):
        self.frame=Toplevel()
        self.frame.title('ComStore Pro (Users)')
        self.frame.wm_attributes("-top", 1)
        self.frame.focus_set()
        self.frame.grab_set()
        self.frame.geometry("1000x500+250+200")

        _init_toolbar(self)
        self._init_gridbox()
        self.frm_addUser=None
        self.frm_editUser=None
        self.addUserflag=False # frmaddUser doesn't exist
        self.editUserflag=False

    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',3),('Username', 25), ('Contact', 10),('Amin',5)))
        #tbUsers=sql.session._query("select * from inventory_User")
        #for p in User.select():print(p.id,p.username)

        self.update_mlb(items=User.select())
        self.mlb.pack(expand=YES,fill=BOTH)
        self.mlb.focus_set()
        self.mlb.bind("<Down>",self.onEntryDown)
        self.frame.bind("<Escape>",self.close_form)
        self.frame.bind("<KeyPress>",self.btn_add_click_keypress)
        self.tb_entryfind.bind("<KeyRelease>",self.tb_btnfind_click)#<Key>",self.keypressed)


    def close_form(self,event):
        #if event.keycode ==27:
        self.frame.destroy()


    def onEntryDown(self, event):
        self.selection = 0
        if event.keycode == 13:
            self.mlb.selection_set(self.selection)
            if self.selection < self.mlb.size()-1:
                self.mlb.selection_clear(self.selection)
                self.selection += 1
                self.mlb.selection_set(self.selection)

##    def OnEntryUp(self, event):
##    if self.selection > 0:
##        self.e1.select_clear(self.selection)
##        self.selection -= 1
##        self.e1.select_set(self.selection)

    # form User add button clicked()
    def btn_add_click(self):
        if self.addUserflag: return 0
        #print ('not exist')
        self.addUserflag=True
        self.frm_addUser=FormAddUser()
        self.frame.wait_window(self.frm_addUser.frame)
        if self.frm_addUser._okbtn_clicked==1:
            self.update_mlb(User.select())
        self.addUserflag=False


    def btn_add_click_keypress(self,event):
        if event.keycode == 97:  # <a>
            self.btn_add_click()
        elif event.keycode == 101: # <e>
            self.btn_edit_click()
        elif event.keycode == 100:  # <d>
            self.btn_del_click()

    def btn_edit_click(self):
        if self.editUserflag: return 0
        #print ('not exist')
        self.editUserflag=True
        self.frm_editUser=FormEditUser()
        item=User.get(User.id == self.mlb.item_selected[1])
        self.frm_editUser.init_entryboxes(self.mlb.item_selected[1:])#(id,username,contact,admin)
        self.frame.wait_window(self.frm_editUser.frame)
        if self.frm_editUser._okbtn_clicked==1:
            self.update_mlbitem(self.mlb.item_selected[0],item)
            item.delete_instance()
        self.editUserflag=False


    def btn_del_click(self):
        try:
            if self.mlb.item_selected==None: return showinfo('info','please select item first',parent=self.frame)
            # sql.session._delete_User(int(self.mlb.item_selected[1]))
            item=User.get(User.id == self.mlb.item_selected[1])
            msg = messagebox.askquestion('warning','Are you sure you want to delete'+' '+str(self.mlb.item_selected[2]),
                    icon='warning',parent=self.frame)
            if msg == 'yes':
                item.delete_instance()
                self.mlb.delete(self.mlb.item_selected[0])
                self.mlb.item_selected=None
            else:
                return
        except ValueError:
            showinfo("Sorry","There isnt any to delete",parent=self.frame)

    # def tb_btnfind_click(self):
    #     #print('sadfsdadf')
    #     fnd=self.tb_entryfind.get()
    #     items = User.select().where(User.username.contains(fnd)).order_by(User.username)
    #     self.mlb.delete(0,END)
    #     for p in items:
    #         self.mlb.insert(END, (p.id,p.username,p.contact,p.is_admin))
    #     self.mlb.selection_set(0) #set first row selected

    def tb_btnfind_click(self,event):
        self.update_mlbb()

    def update_mlbb(self):
        fnd=self.tb_entryfind.get()
        items = User.select().where(User.username.contains(fnd)).order_by(User.username)
        self.mlb.delete(0,END)
        for p in items:
            self.mlb.insert(END, (p.id,p.username,p.contact,p.is_admin))
        self.mlb.selection_set(0) #set first row selected

    def update_mlb(self,items):
        self.mlb.delete(0,END)

        for p in items:
            self.mlb.insert(0, (p.id,p.username,p.contact,p.is_admin))
        self.mlb.selection_set(0) #set first row selected

    def update_mlbitem(self,index,p):
        self.mlb.delete(index)
        self.mlb.insert(index, (p.id,p.username,p.contact,p.is_admin))
        self.mlb.selection_set(index) #set item edited

##    def update_mlbitem(self,index,items):
##        self.mlb.delete(index)
##        for p in items:
##            self.mlb.insert(index, (p.id,p.username,p.contact,p.is_admin))
##        self.mlb.selection_set(index) #set item edited


class FormAddUser:
    '''Add New User three labels and three textboxes and an OK button'''
    def __init__(self):

        self.frame=Toplevel()
        #self.frame.geometry("330x100+250+200")
        #self.frame.wm_transient()
        self.frame.wm_attributes("-top", 2)
        self.frame.grab_set()
        self.frame.geometry("200x150+600+400")
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()

    def _init_widgets(self):
        self.label1=Label(self.frame,text="User:")
        self.label1.grid(row=0, column=0,sticky=W)
        self.entry1=Entry(self.frame)
        self.entry1.grid(row=0,column=1)
        self.entry1.focus()

        validation = self.frame.register(self.only_numbers)

        Pwd = '{:03}'.format(rand.randrange(1, 10**6))
        self.label2=Label(self.frame,text="Contact:")
        self.label2.grid(row=1,column=0,sticky=W)
        self.entry2=Entry(self.frame,validate="key", validatecommand=(validation, '%S'))#,highlightthickness=2,highlightbackground="blue")
        self.entry2.grid(row=1,column=1)


        self.label3=Label(self.frame,text="Password:")
        self.label3.grid(row=2,sticky=W,column = 0)
        self.entry3=Entry(self.frame)
        self.entry3.grid(row=2,sticky=W,column=1)
        self.entry3.insert(END,randomStringDigits(8))



        self.label4=Label(self.frame,text="Admin:")
        self.label4.grid(row=3,column=0,sticky=W)
        self.entry4 = ttk.Combobox(self.frame,values=["yes","no"])
        self.entry4.grid(row=3,column=1,sticky=W)
        self.entry4.current(1)


##        self.entry4=Entry(self.frame)
##        self.entry4.grid(row=3,column=1)

        #self.entry3.bind("<Return>", lambda e: self.btnok_click())

        self.frame1=Frame(self.frame)
        self.btn_ok=Button(self.frame1,text="Ok",width=7,command=self.btnok_click)
        self.btn_ok.pack(side=RIGHT)
        self.btn_ok.bind("<Return>",lambda e: self.btnok_click())

##        self.btn_cancel=Button(self.frame1,text="Cancel",width=7,command=self.close)
##        self.btn_cancel.pack(side=RIGHT)
##        self.btn_cancel.bind("<Return>",self.frame.destroy)
        self.frame1.grid(row=4,column=1,sticky=E)
        self.frame.bind("<KeyPress>",self.close_form)

    # validate contact entry function
    def only_numbers(self,char):
        return char.isdigit()

    def close(self):
        self.frame.destroy()

    def close_form(self, event):
        if event.keycode==27:
            self.frame.destroy()
        elif event.keycode ==13:
            self.btnok_click

    def btnok_click(self):
        verify = User.select()
        usernames = [];passwords = []
        for user in verify:
            usernames.append(user.username)
            passwords.append(user.password)
        items=(self.entry1.get(),self.entry3.get(),self.entry2.get(),self.entry4.get())
        if '' in items:
            showinfo("info", "No user added!\nAll entries required",parent=self.frame)
            return 0

        if self.entry1.get() in usernames: showinfo("Info", "User already exists",parent=self.frame);return 0
        elif self.entry3.get() in passwords: showinfo("Info", "Password already exists",parent=self.frame); return 0
        else: p = User.create(username=items[0],password=generate_password_hash(items[1],"sha256"),contact=int(items[2]),is_admin=items[3])
        self._okbtn_clicked=1
        showinfo(" ", "Welcome! Username & password successfully created.",parent=self.frame)
        self.sms()
        self.frame.destroy()

    def callback(self):
        self._okbtn_clicked=0
        #print ('user exits the screen')
        self.frame.destroy()

    def sms(self):
        import nexmo
        pwd = self.entry4.get()
        username = self.entry1.get()
        msg = "Your logins\nUsername:"+""+username+"\n"+"Password:"+""+pwd
        try:
            client = nexmo.Client(key='e9d6bfb6', secret='OUJ8GmGwPRQmnAQ4')
            client.send_message({
                        'from': 'ComStore Pro',
                        'to': self.entry2.get(),
                        'text': msg,
                    })
        except:
            messagebox.showerror("Error","No Internet to receive sms\nTry:\n   Reconnecting to internet",parent=self.frame)



class FormEditUser:
    '''Add New User three labels and three textboxes and an OK button'''
    def __init__(self):

        self.frame=Toplevel()
        #self.frame.geometry("330x100+250+200")
        #self.frame.wm_transient()
        self.frame.wm_attributes("-top", 2)
        self.frame.grab_set()
        self.frame.geometry("200x150+600+400")
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()

    def _init_widgets(self):
        self.label1=Label(self.frame,text="User:")
        self.label1.grid(row=0, column=0,sticky=W)
        self.entry1=Entry(self.frame)
        self.entry1.grid(row=0,column=1)
        self.entry1.focus()


        validation = self.frame.register(self.only_numbers)


        self.label2=Label(self.frame,text="Contact:")#,validate="key", validatecommand=(validation, '%S'))#,highlightthickness=2,highlightbackground="blue")
        self.label2.grid(row=1,column=0,sticky=W)
        self.entry2=Entry(self.frame)
        self.entry2.grid(row=1,column=1)

        self.label3=Label(self.frame,text="Password:")
        self.label3.grid(row=2,sticky=W,column = 0)
        self.entry3=Entry(self.frame)
        self.entry3.grid(row=2,sticky=W,column=1)

        self.label4=Label(self.frame,text="Admin:")
        self.label4.grid(row=3,column=0,sticky=W)
        self.entry4 = ttk.Combobox(self.frame,values=["yes","no"])
        self.entry4.grid(row=3,sticky=W,column=1)
        #self.entry4.current(1)

##        self.label4=Label(self.frame,text="Admin:")
##        self.label4.grid(row=3,column=0,sticky=W)
##        self.entry4=Entry(self.frame)
##        self.entry4.grid(row=3,column=1)

        self.entry3.bind("<Return>", lambda e: self.btnok_click())

        self.frame1=Frame(self.frame)
        self.btn_ok=Button(self.frame1,text="Ok",width=7,command=self.btnedit_click)
        self.btn_ok.pack(side=RIGHT)
        self.btn_ok.bind("<Return>",lambda e: self.btnok_click())


        #self.entry3.bind("<Return>", lambda e: self.btnok_click())

##        self.btn_cancel=Button(self.frame1,text="Cancel",width=7,command=self.close)
##        self.btn_cancel.pack(side=RIGHT)
##        self.btn_cancel.bind("<Return>",self.frame.destroy)
        self.frame1.grid(row=4,column=1,sticky=E)
        self.frame.bind("<KeyPress>",self.close_form)

    # validate contact entry function
    def only_numbers(self,char):
        return char.isdigit()

    def close(self):
        self.frame.destroy()

    def close_form(self, event):
        if event.keycode==27:
            self.frame.destroy()
        elif event.keycode ==13:
            self.btnok_click

    def btnedit_click(self):
        items=(self.entry1.get(),self.entry3.get(),self.entry2.get(),self.entry4.get())
        if '' in items:
            showinfo("info", "Editing failed!\nAll entries required",parent=self.frame)
            return 0

        p = User.create(username=items[0],password=generate_password_hash(items[1],"sha256"),contact=int(items[2]),is_admin=items[3])
        self._okbtn_clicked=1
        showinfo(" ", "Password changed!", parent=self.frame)
        #self.sms()
        self.frame.destroy()

    def callback(self):
        self._okbtn_clicked=0
        #print ('user exits the screen')
        self.frame.destroy()

    def init_entryboxes(self,val):
        pwd = '{:03}'.format(rand.randrange(1, 10**6))
        self.entry4.insert(END,val[3])#admin
        self.entry3.insert(END,randomStringDigits(8))#password
        self.entry2.insert(END,val[2])#contact
        self.entry1.insert(END,val[1])#Username

    def sms(self):
        import nexmo
        try:
            client = nexmo.Client(key='e9d6bfb6', secret='OUJ8GmGwPRQmnAQ4')
            client.send_message({
                        'from': 'ComStore Pro',
                        'to': self.entry2.get(),
                        'text': self.entry3.get(),
                    })
        except:
            messagebox.showerror("Error","No Internet to receive sms\nTry reconnecting to internet",parent=self.frame)

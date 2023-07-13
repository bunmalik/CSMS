#import modules
# src: https://www.simplifiedpython.net/python-gui-login/

from tkinter import *
from tkinter import ttk
from forms import home
from tkinter.messagebox import *
from models import Users as User
from models import States
from werkzeug.security import check_password_hash

import time
import queue
import threading
import random as rand
import nexmo
import models
import pickle
import os

models.create_tables_if_not_exist()
client = nexmo.Client(key='e9d6bfb6', secret='OUJ8GmGwPRQmnAQ4')
FILENAME = "save.pickle"
# Designing window for registration

class Login:

    def __init__(self,master):
        self.frame=master
        self.frame.geometry("500x300+500+300")
        self.frame.title("ComStore Pro")
        self.frame.resizable(0,0)
        self.main_account_screen()
        self.restore_state()
        self.staff = None
        self.attempt1 = 0
        self.attempt2 = 0
        self.count1 = 4
        self.count2 = 4


    def main_account_screen(self):
        global main_screen
        global but
        global log
        main_screen = Frame(self.frame)
        Label(self.frame,text='Welcome to Computer Store Management System\n(ComStore Pro)',bg="blue", width="300", height="2",foreground="white", font=("Calibri", 13)).pack()
        Label(self.frame,text="Select To login or Register", bg="blue", width="300", height="2", foreground="white",font=("Calibri", 15)).pack()
        Label(self.frame,text="").pack()
        log = Button(self.frame,text="Login", height="2", width="30", command = self.login)
        log.pack()
        log.focus_set()
        log.bind("<KeyPress>",self.main_screen_butlogin)
        Label(self.frame,text="").pack()
        but = Button(self.frame,text="Admin", height="2", width="30", command=self.admin)
        but.bind("<KeyPress>",self.main_screen_butadmin)
        but.pack()
        butcancelmainloop = Button(self.frame,text="Cancel", height="2", width="10", bg="orange",command=self.save_state)
        butcancelmainloop.pack(side=BOTTOM)
        butcancelmainloop.bind("<KeyPress>",self.main_screen_butcancel)
        self.frame.bind("<Escape>",self.main_screen_keypress)
        main_screen.pack()
        self.frame.protocol("WM_DELETE_WINDOW", self.save_state)
        #stat = States.create(login='login',admin="nod")

    def save_state(self):
        data = {
            "login": log['state'],
            "admin": but['state'],
        }


        try:
            data = {
                "login": log['state'],
                "admin": but['state'],
            }
            with open("save.txt", "w") as f:
                f.write(data['login']+'\n'+data['admin'])
            self.frame.destroy()
        except Exception as e:
            print(e)
            pass

    def restore_state(self):
        try:
            with open("save.txt", "r") as f:
                state = f.read().splitlines()
            log['state'] = state[0]
            but['state'] = state[1]
        except Exception as e:
            pass



    def admin(self):
        global admin_login_screen
        global admin_login_entry
        global password_login_entry
        admin_login_screen = Toplevel(main_screen)
        admin_login_screen.title("Admin login")
        admin_login_screen.geometry("300x300+500+300")
        admin_login_screen.wm_attributes("-top", 1)
        #admin_login_screen.grab_set()
        admin_login_screen.resizable(0,0)
        admin_login_screen.wm_attributes('-fullscreen', False)
        Label( admin_login_screen, text="Admin login",bg="blue",fg="white",font=("Calibri", 14,"bold")).pack()
        Label( admin_login_screen, text="").pack()

        global admin_verify
        global admin_pwd_verify

        admin_verify = StringVar()
        admin_pwd_verify = StringVar()

        global admin_login_entry
        global admin_pwd_entry

        Label( admin_login_screen, text="Admin name * ").pack()
        admin_login_entry = Entry( admin_login_screen, textvariable=admin_verify)
        admin_login_entry.pack()
        admin_login_entry.focus_set()
        Label( admin_login_screen, text="").pack()
        Label( admin_login_screen, text="Password * ").pack()
        admin_pwd_entry = Entry( admin_login_screen, textvariable=admin_pwd_verify, show= '*')
        admin_pwd_entry.pack()
        Label( admin_login_screen, text="").pack()

        butlogin = Button( admin_login_screen, text="Login", width=12, height=1, bg="blue",fg="white",font=("Calibri", 13),command = self.verify_admin)
        butlogin.pack()
        #butlogin.bind("<KeyPress>",login_keypress)
        #butlogin.bind("<KeyRelease>",login_keypress)
        Label( admin_login_screen, text="").pack()
        butforgotpassword = Button( admin_login_screen, text="forgot password?", width=12, height=1, command = self.forgotadminpassword)
        butforgotpassword.pack()
        #butforgotpassword.bind("<KeyPress>",self.forgotpassword_keypress)
        butcancel = Button( admin_login_screen,text="Cancel", height="1", width="12", bg="orange" ,command=admin_login_screen.destroy)
        butcancel.pack(side='bottom')
        #butcancel.bind("<KeyPress>",self.cancel_keypress)
        admin_login_screen.bind("<KeyPress>",self.admin_login_screen_keypress)

    def admin_login_screen_keypress(self,event):
        if event.keycode == 13:
            self.verify_admin()
        if event.keycode == 27:
            admin_login_screen.destroy()

    def verify_admin(self):
        admin_info = admin_login_entry.get()
        pwd_info = admin_pwd_entry.get()

        verify = User.select().where(User.is_admin.contains("yes"))
        self.attempt1 = self.attempt1 + 1
        self.count1 = self.count1 - 1
        adminnames = [];passwords = []
        for user in verify:
            adminnames.append(user.username)
            passwords.append(user.password)

        if self.attempt1 > 4:
            showerror("Error","Too many attempts\nSee Shop Owner",parent=admin_login_screen)
            admin_login_screen.destroy()
            log.config(state="disabled")
            but.config(state="disabled")
##            self.attempt1=0
##            self.count1 =4
        else:
            if admin_info =='' or pwd_info=='':
                showerror("Error", "All fields required\n\nYou have"+" "+str(self.count1)+" "+"attempts left\n\nTry again!",parent=admin_login_screen)
                admin_login_entry.focus_set()
            else:
                if any(admin_info == adminnames[i] and check_password_hash(passwords[i],pwd_info)==True for i in range(0,len(passwords))):

                    if any(check_password_hash(passwords[i],pwd_info)==True for i in range(0,len(passwords))):#pwd_info in passwords:
                        showinfo("info", "Login Success",parent=admin_login_screen)
                        self.manage()
                        file1 = open('Staff', "w")
                        file1.write(admin_info)
                        file1.close()
                        admin_login_screen.destroy()
                    else:
                        showerror("Sorry", "Invalid password!\n\nYou have"+" "+str(self.count1)+" "+"attempts left\n\nTry again!",parent=admin_login_screen)
                else:
                    showerror("Error","Admin not found\n\nYou have"+" "+str(self.count1)+" "+"attempts left\n\nTry again!",parent=admin_login_screen)





    def manage(self):
        global manage_screen
        manage_screen = Toplevel(main_screen)
        manage_screen.title("Admin login")
        manage_screen.geometry("300x200+500+300")
        manage_screen.wm_attributes("-top", 1)
        manage_screen.grab_set()
        manage_screen.resizable(0,0)
        manage_screen.wm_attributes('-fullscreen', False)
        Label( manage_screen, text="Select Your Choice",bg="blue",fg="white",font=("Calibri", 14,"bold")).pack()
        Label( manage_screen, text="").pack()

        enable_login_button= Button(manage_screen, text="Enable User login", width=20, height=1,font=("Calibri", 13),command = self.enable_user_login)
        enable_login_button.pack()
        #enable_login_button.bind("<KeyPress>",login_keypress)
        #enable_login_button.bind("<KeyRelease>",login_keypress)
        Label( admin_login_screen, text="").pack()
        Label( manage_screen, text="").pack()
        go_to_home_button = Button(manage_screen, text="Go to home", width=20, height=1, font=("Calibri", 13),command = self.admin_login)
        go_to_home_button.pack()
        #go_to_home_button.bind("<KeyPress>",self.forgotpassword_keypress)
        cancel = Button(manage_screen,text="Close",height="2",width="10",command=manage_screen.destroy)
        cancel.pack(side=BOTTOM)

    def enable_user_login(self):
        manage_screen.destroy()
        #main_screen.deiconify()
        log["state"]="active"



    def admin_login(self):
        self.home=home.FormMenu()
        manage_screen.destroy()
##        admin_login_screen.destr
##        self.frame.wait_window(self.home.frame)
##        admin_login_screen.deiconify()


    def register(self):
        global register_screen
        register_screen = Toplevel(main_screen)
        register_screen.title("Register")
        register_screen.lift()
        register_screen.grab_set()
        #register_screen.geometry("300x250")
        register_screen.geometry("300x250+500+300")
        register_screen.resizable(0,0)
        register_screen.wm_attributes('-fullscreen', False)

        global username
        global password
        global contact
        global username_entry
        global password_entry
        global contact_entry
        global username_lable
        username = StringVar()
        password = StringVar()
        contact = IntVar()

        Label(register_screen, text="Please enter details below", bg="blue").pack()
        Label(register_screen, text="").pack()
        username_lable = Label(register_screen, text="Username * ")
        username_lable.pack()
        username_entry = Entry(register_screen, textvariable=username,highlightthickness=2, highlightbackground="blue", selectbackground="yellow", highlightcolor='#4584F1')
        username_entry.pack()
        username_entry.focus_set()
        password_lable = Label(register_screen, text="Password * ")
        password_lable.pack()
        password_entry = Entry(register_screen, textvariable=password, show='*',highlightthickness=2,highlightbackground="blue")
        password_entry.pack()
        contact_lable = Label(register_screen, text="Contact * ")
        contact_lable.pack()
        validation = register_screen.register(self.only_numbers)
        contact_entry = Entry(register_screen, validate="key", validatecommand=(validation, '%S'),highlightthickness=2,highlightbackground="blue")
        contact_entry.pack()
        Label(register_screen, text="").pack()
        butregisteruser = Button(register_screen, text="Register", width=10, height=1, bg="blue")
        butregisteruser.pack()
        butregisteruser.bind("<KeyPress>", self.register_user_keypress )
        butcancel = Button(register_screen,text="Cancel", height="1", width="10", bg="orange",command=register_screen.destroy)
        butcancel.pack(side='bottom')
        butcancel.bind("<KeyPress>", self.register_keypress )
        register_screen.bind("<KeyPress>", self.register_screen_keypress)
        register_screen.focus_set()

    # validate contact entry function
    def only_numbers(self,char):
        return char.isdigit()

    def register_screen_keypress(self,event):
        if event.keycode ==27:
            register_screen.destroy()

    def register_keypress(self,event):
        if event.keycode ==13:
            register_screen.destroy()
        elif event.keycode ==27:
            register_screen.destroy()

    def register_user_keypress(self,event):
        if event.keycode ==13:
            self.register_user()
    # Designing window for login

    def login(self):
        global login_screen
        global username_login_entry
        global password_login_entry
        login_screen = Toplevel(main_screen)
        login_screen.title("Login")
        login_screen.geometry("300x300+500+300")
        login_screen.wm_attributes("-top", 1)
        login_screen.grab_set()
        login_screen.resizable(0,0)
        login_screen.wm_attributes('-fullscreen', False)
        Label(login_screen, text="Please provide login details below",bg="blue",fg="white",font=("Calibri", 13,"bold")).pack()
        Label(login_screen, text="").pack()

        global username_verify
        global password_verify

        username_verify = StringVar()
        password_verify = StringVar()

        global username_login_entry
        global password_login_entry

        Label(login_screen, text="Username * ").pack()
        username_login_entry = Entry(login_screen, textvariable=username_verify)
        username_login_entry.pack()
    ##    list_of_files = os.listdir()
    ##    username_login_entry.insert(END,list_of_files[0])
        username_login_entry.focus_set()
        Label(login_screen, text="").pack()
        Label(login_screen, text="Password * ").pack()
        password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
        password_login_entry.pack()
        #password_login_entry.focus()
        Label(login_screen, text="").pack()

        butlogin = Button(login_screen, text="Login", width=12, height=1, bg="blue",fg="white",font=("Calibri", 13),command = self.login_verify)
        butlogin.pack()
        #butlogin.bind("<KeyPress>",login_keypress)
        #butlogin.bind("<KeyRelease>",login_keypress)
        Label(login_screen, text="").pack()
        butforgotpassword = Button(login_screen, text="forgot password?", width=12, height=1, command = self.forgotuserpassword)
        butforgotpassword.pack()
        #butforgotpassword.bind("<KeyPress>",self.forgotpassword_keypress)
        butcancel = Button(login_screen,text="Cancel", height="1", width="12", bg="orange" ,command=login_screen.destroy)
        butcancel.pack(side='bottom')
        butcancel.bind("<KeyPress>",self.cancel_keypress)
        login_screen.bind("<KeyPress>",self.login_screen_keypress)

    def forgotuserpassword(self):
        showinfo("Info", "See Admin for password reset",parent=login_screen)

    def login_keypress(self,event):
        if event.keycode == 13: # <Enter>
            self.login_verify()


    def forgotpassword_keypress(self,event):
        if event.keycode == 13: # <Enter>
            self.forgotuserpassword()


    def cancel_keypress(self,event):
        if event.keycode == 13: # <Enter>
            login_screen.destroy()

    def login_screen_keypress(self,event):
        if event.keycode == 27: # <Escape>
            login_screen.destroy()
        elif event.keycode ==13:
            self.login_verify()


    # Implementing event on register button
    def register_user(self):

        username_info = username.get()
        password_info = password.get()
        contact_info = contact_entry.get()

        list_of_files = os.listdir()

        if username_info =='' or password_info=='' or contact_info =='':
            #user_not_registered()
            showerror("Error", "All fields required",parent=register_screen)
            username_entry.focus_set()
        else:
            items=(username_info,password_info,contact_info)
            p = User.create(username=items[0],password=items[1],contact=int(items[2]))
            if username_info ==p.select().where(User.username.contains(username_info))[0].username:
                username_lable.configure(text="User exists", fg = 'red')
                username_entry.configure(highlightbackground='red', highlightcolor='red')
                username_entry.delete(0, END)
                username_entry.focus_set()
            elif password_info == p.select().where(User.username.contains(password_info))[0].password:
                password_lable.configure(text="Password exists", fg = 'red')
                password_entry.configure(highlightbackground='red', highlightcolor='red')
                password_entry.delete(0, END)
                password_entry.focus_set()
            elif contact_info == p.select().where(User.username.contains(contact_info))[0].contact:
                contact_lable.configure(text="Contact exists", fg = 'red')
                contact_entry.configure(highlightbackground='red', highlightcolor='red')
                contact_entry.delete(0, END)
                contact_entry.focus_set()
            else:
                showinfo("info", "Registration success",parent=register_screen)
                register_screen.destroy()
                but['state']=DISABLED




##    @classmethod
##    def create_user(cls, username, email, password, admin=False):
##        try:
##            with DATABASE.transaction():
##              cls.create(
##                  username=username,
##                  email=email,
##                  password=generate_password_hash(password),
##                  is_admin=admin)
##        except IntegrityError:
##            raise ValueError("User already exists")

    def forgotadminpassword(self):
        global entry
        global password_reset
        global validation
        global sending

        password_reset = Toplevel(admin_login_screen)
        password_reset.title("Reset password")
        password_reset.geometry("300x150+700+350")
        password_reset.wm_attributes("-top", 1)
        password_reset.resizable(0,0)
        password_reset.wm_attributes('-fullscreen', False)
        password_reset.grab_set()

        Label(password_reset, text = "please enter your contact for verification", bg='blue',fg="white",font=("Calibri", 12,'bold')).pack()
        Label(password_reset, text = " ").pack()

        validation = password_reset.register(self.only_numbers)

        frame1 = Frame(password_reset)
        Label(frame1, text='Contact: ').pack(side='left')
        entry = Entry(frame1, validate="key", validatecommand=(validation, '%S'),highlightthickness=2,highlightbackground="blue")
        entry.pack(side='left')
        entry.focus()
        Label(frame1, text=' ' ).pack(side='left')
        Button(frame1, text='ok', width = 2, height=1, command=self.verify_contact).pack(side=LEFT)
        entry.delete(0, END)
        frame1.pack()
        sending = Label(password_reset, text = "  ", fg="green", font=("calibri", 11))
        sending.pack()
        Button(password_reset, text='cancel',bg='orange', command=password_reset.destroy).pack(side='bottom')
        password_reset.bind("<KeyPress>",self.verify_contact_keypress)

    def verify_contact_keypress(self,event):
        if event.keycode ==13:
            self.verify_contact()
        elif event.keycode ==27:
            password_reset.destroy()

    def verify_contact(self):
        global code
        customer_id = "09DE1769-4B49-449E-92DA-72F2E7AD7B39"
        api_key = "3a0WGzTA6Wa4eGnz80u52LxZleCC7RUChLek1T5ZQuBFGkqZUwyQFTU7ijlJql+l9Y9EMTSi6yJortsxs3/Pdw=="

        try:
##            file1 = open('Passwords', "r")
##            verify = file1.read().splitlines()
            verify = User.select()
            usernames = [];passwords = []
            for user in verify:
                usernames.append(user.contact)
            contact = entry.get()

            if int(contact) in usernames:
                sending.config(text = "Sending SMS...")
                sending.update_idletasks()
                code = '{:03}'.format(rand.randrange(1, 10**3))+'-'+'{:03}'.format(rand.randrange(1, 10**3))
                msg = code+' '+'is your verification code\nValid for 5 mins'
                print(msg)
##                client.send_message({
##                    'from': 'ComStore Pro',
##                    'to': '+233'+entry.get(),
##                    'text': msg,
##                })
    ##            message_type = "ARN" # OPT ARN OR MKT
    ##            messaging = MessagingClient(customer_id, api_key)
    ##            response = messaging.message('+233'+entry.get(), msg, message_type)
    ##            sending.config(text = "Done!")
                time.sleep(5)
                password_reset.destroy()
                self.verify_code()

            else:
                showinfo("info", "Contact not available in our system",parent=password_reset)
                entry.delete(0,END)
        except FileNotFoundError:
             showinfo("info", "Contact not registered \n Provide your details in the registration form",parent=password_reset)
             password_reset.destroy()
             admin_login_screen.destroy()
##        except:
##            showinfo("Info","No connection", parent=login_screen)
##            password_reset.destroy()



    def verify_code(self):
        global code_verify
        global verifying
        global cod
        code_verify = Toplevel(admin_login_screen)
        code_verify.title("verify")
        code_verify.geometry("300x70+700+350")
        code_verify.wm_attributes("-top", 1)
        code_verify.resizable(0,0)
        code_verify.wm_attributes('-fullscreen', False)
        code_verify.grab_set()
        code_verify.config(cursor="wait")


        frame2 = Frame(code_verify)
        Label(frame2, text = "Code:  ").pack(side='left')
        cod = Entry(frame2,validate="key", validatecommand=(validation, '%S'),highlightthickness=2,highlightbackground="blue")
        cod.pack(side = 'left')
        cod.focus()
        cod.delete(0, END)

        Label(frame2, text=' ').pack(side = 'left')
        button_verify = Button(frame2, text='Verify',command=self.busy)
        button_verify.pack(side='left')
        frame2.pack()
        verifying = Label(code_verify,text=' ', fg = 'green',font=("calibri", 11))
        verifying.pack()
        Button(code_verify, text='cancel',bg='orange',command=code_verify.destroy).pack(side='bottom')
        code_verify.bind("<KeyPress>",self.verify_code_keypress)
        code_verify.after(5*10000,lambda: code_verify.destroy())


    def verify_code_keypress(self,event):
        if event.keycode == 13:
            self.busy()
        elif event.keycode == 27:
            code_verify.destroy()


    def busy(self):
        verifying.config(text='verifying...')
        verifying.update_idletasks()
        time.sleep(3)

        if cod.get() == code:
           verifying.config(text='verified')
           verifying.update_idletasks()
           #main_screen.config(cursor="wait")
           time.sleep(2)
           code_verify.destroy()
           admin_login_screen.destroy()
           log.config(state="active")
           but.config(state='active')
        else:
           showerror('error','wrong code',parent=code_verify);verifying.config(text=' ')
           cod.delete(0,END)

        #main_screen.config(cursor="wait")




    def user_not_registered(self):
        global register_error
        register_error = Toplevel(register_screen)
        register_error.title("error")
        register_error.geometry("300x50+700+350")
        register_error.wm_attributes("-top", 1)
        register_error.resizable(0,0)
        register_error.wm_attributes('-fullscreen', False)
        register_error.grab_set()
        Label(register_error, text="All fields required").pack()
        Button(register_error, text="OK", command=self.register_error.destroy).pack()


    # Implementing event on login button
    def login_verify(self):
        #list_of_files = os.listdir()
        try:
            username1 = username_verify.get()
            password1 = password_verify.get()
            username_login_entry.delete(0, END)
            password_login_entry.delete(0, END)

#            file1 = open('Passwords', "r")
##            verify = file1.read().splitlines()
            verify = User.select()
            usernames = [];passwords = []
            for user in verify:
                usernames.append(user.username)
                passwords.append(user.password)
                            #login_i ==p.select().where(User.username.contains(username_info))[0].username:

            self.attempt2 = self.attempt2 + 1
            self.count2 = self.count2 - 1

            if self.attempt2 > 4:
                showerror("Error","Too many attempts\nSee Admin to register",parent=login_screen)
                login_screen.destroy()
                log.config(state="disabled")
                self.attempt2=0
                self.count2 =4

            else:
                if any(username1 == usernames[i] and check_password_hash(passwords[i],password1)==True for i in range(0,len(passwords))):
                    if any(check_password_hash(passwords[i],password1)==True for i in range(0,len(passwords))):
                        self.login_sucess()
                        file1 = open('Staff', "w")
                        file1.write(username1)
                        file1.close()
                    else:
                        #self.password_not_recognised()
                        showerror("Password error","Password not recognised"+"\n\nYou have"+" "+str(self.count2)+" "+"attempts left\n\nTry again!",parent=login_screen)
                else:
                    #self.user_not_found()
                    showerror("User error", "User not found"+"\n\nYou have"+" "+str(self.count2)+" "+"attempts left\n\nTry again!",parent=login_screen)

        except FileNotFoundError as error:
            showinfo('info','Please register first',parent=login_screen)


    # Designing popup for login success

    def login_sucess(self):
        global login_success_screen
        login_success_screen = Toplevel(login_screen)
        login_success_screen.title("Success")
        login_success_screen.geometry("150x80+700+350")
        login_success_screen.wm_attributes("-top", 1)
        login_success_screen.resizable(0,0)
        login_success_screen.attributes('-fullscreen', False)
        login_success_screen.grab_set()
        Label(login_success_screen, text="Login Success").pack()
        butok = Button(login_success_screen, text="OK", command=self.login_success_open_homeform)
        butok.pack()
        butok.bind("<KeyPress>",self.login_success_keypress)
        login_success_screen.bind("<KeyPress>",self.login_success_keypress)
        login_success_screen.focus_set()

    def login_success_keypress(self,event):
        if event.keycode == 13:
            self.login_success_open_homeform()
        elif event.keycode == 27:
            login_success_screen.destroy()

    # opening home form if successfully logged in

    def login_success_open_homeform(self):
        login_success_screen.destroy()
        login_screen.destroy()
        models.create_tables_if_not_exist()
        self.frame.withdraw()
        frmmenu = home.FormMenu()
        self.frame.wait_window(frmmenu.frame)
        self.frame.deiconify()

        #print ("products")
        #self.frame.withdraw()
        #self.frm_products=FormProducts()
        #self.frame.wait_window(self.frm_products.frame)
        #self.frame.deiconify()


    def password_not_recognised_keypress(self,event):
        if event.keycode == 13:
            self.delete_password_not_recognised()



    # Designing popup for login invalid password

    def password_not_recognised(self):
        global password_not_recog_screen
        password_not_recog_screen = Toplevel(login_screen)
        password_not_recog_screen.title("Access denied")
        password_not_recog_screen.geometry("150x100+500+300")
        password_not_recog_screen.resizable(0,0)
        password_not_recog_screen.wm_attributes('-fullscreen', False)
        password_not_recog_screen.wm_attributes("-top", 1)
        password_not_recog_screen.grab_set()
        Label(password_not_recog_screen, text="Invalid Password ").pack()
        Button(password_not_recog_screen, text="OK", command=self.delete_password_not_recognised).pack()
        password_not_recog_screen.bind("<KeyPress>",self.password_not_recognised_keypress)
        password_not_recog_screen.focus_set()


    # Designing popup for user not found

    def user_not_found(self):
        global user_not_found_screen
        user_not_found_screen = Toplevel(login_screen)
        user_not_found_screen.title("Success")
        user_not_found_screen.geometry("150x100+500+300")
        user_not_found_screen.resizable(0,0)
        user_not_found_screen.wm_attributes('-fullscreen', False)
        user_not_found_screen.wm_attributes("-top", 1)
        user_not_found_screen.grab_set()
        Label(user_not_found_screen, text="User Not Found").pack()
        Button(user_not_found_screen, text="OK", command=self.delete_user_not_found_screen).pack()
        user_not_found_screen.focus_set()
        user_not_found_screen.bind("<KeyPress>",self.user_not_found_keypress)

    def user_not_found_keypress(self,event):
        if event.keycode == 13:
            self.delete_user_not_found_screen()

    def delete_password_not_recognised(self):
        password_not_recog_screen.destroy()


    def delete_user_not_found_screen(self):
        user_not_found_screen.destroy()

    def main_screen_keypress(self,event):
        if event.keycode == 27: # <Escape>
            main_screen.destroy()

    def main_screen_butcancel(self,event):
        if event.keycode == 13: # Enter key
            self.frame.destroy()

    def main_screen_butlogin(self,event):
        if log["state"]=="disabled": return
        if event.keycode == 13:
            self.login()
    def main_screen_butadmin(self,event):
        if but["state"]=="disabled": return
        if event.keycode == 13:
            self.admin()

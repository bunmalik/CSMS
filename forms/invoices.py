from tkinter import *
from tkinter.ttk import *
from modules.tklistview import MultiListbox
from modules.tktoolbar import _init_toolbar,_init_stafftoolbar
from forms.addinvoice import FormAddInvoice
from models import Inventory_Invoice as Invoice
from models import Inventory_InvoiceItem as InvoiceItem
from tkinter.messagebox import showinfo
from tkinter import messagebox
from models import Users as User
from werkzeug.security import check_password_hash
from tkinter.messagebox import showinfo, showerror
import sys
sys.dont_write_bytecode = True

def label_entry(frmlblent,txtlbl,txtlbl2=None):
    label=Label(frmlblent,text=txtlbl)
    label.pack(side=LEFT)
    frmlblent._entry=Entry(frmlblent)
    frmlblent._entry.pack(side=LEFT)
    if txtlbl2:
        label2=Label(frmlblent,text=txtlbl2)
        label2.pack(side=LEFT)
        frmlblent._entry2=Entry(frmlblent)
        frmlblent._entry2.pack(side=LEFT)

class FormInvoices:
    def __init__(self):
        self.frame=Toplevel()
        self.frame.title('ComStore Pro (Invoice)')
        self.frame.geometry("1000x500+250+200")
        self.frame.wm_attributes("-topmost", 1)
        self.frame.focus_set()
        self.frame.grab_set()
        _init_stafftoolbar(self)
        self._init_gridbox()
        self.frm_addinvoice=None
        self.addinvoiceflag=False
        self.editinvoiceflag=False

    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',5),('Customer', 25), ('Date', 15), ('Grand Total', 15)))
        self.update_mlb(Invoice.select())
        self.mlb.pack(expand=YES,fill=BOTH)
        self.frame.bind("<KeyPress>",self.close_form)
        self.tb_entryfind.bind("<KeyRelease>",self.tb_btnfind_click)#<Key>",self.keypressed)


    def close_form(self,event):
        if event.keycode ==27:
            self.frame.destroy()


    def update_mlb(self,tb):
        self.mlb.delete(0,END)
        for i in tb:
            self.mlb.insert(END, (i.id,i.customer,i.date,i.amount))
        self.mlb.selection_set(0) #set first row selected

    def btn_add_click(self):
        try:
            if self.addinvoiceflag:
                showinfo('info','Invoice window exist',parent=self.frame)
                return 0
            self.addinvoiceflag=True
            self.frm_addinvoice=FormAddInvoice()
            self.frame.wait_window(self.frm_addinvoice.frame)
            self.update_mlb(Invoice.select())
            self.addinvoiceflag=False
        except:
            showinfo("Info","Product does not exist",parent=self.frame)
            return '0'

    def btn_edit_click(self):
        try:
            if (self.editinvoiceflag or not self.mlb.item_selected[1]) : return 0
            self.editinvoiceflag=True
            self.frm_editinvoice=FormEditInvoice()
            self.frm_editinvoice.init_entryboxes(self.mlb.item_selected[1:])#(id,customer,date,amount)
            items = InvoiceItem.select().where(InvoiceItem.invoice == int(self.mlb.item_selected[1]))
            self.frm_editinvoice.update_mlbitems(items)
            self.frame.wait_window(self.frm_editinvoice.frame)
            self.editinvoiceflag=False
        except:
            showinfo("info","Product does not exists",parent=self.frame)
            return '0'

    def btn_del_(self):

        if self.mlb.item_selected==None: return showinfo('info','please select item first')
        item = Invoice.get(Invoice.id == self.mlb.item_selected[1])
        msg = messagebox.askquestion('warning','Are you sure you want to delete'+' '+str(self.mlb.item_selected[2]+'?'), icon='warning',parent=self.frame)
        if msg == 'yes':
            item.delete_instance(recursive=True)
            self.mlb.delete(self.mlb.item_selected[0])
            self.mlb.item_selected=None
        else:
            return

    def tb_btnfind_click(self):
        print ('find')

    def tb_btnfind_click(self,event):
        self.update_mlbb()

    def update_mlbb(self):
        fnd=self.tb_entryfind.get()
        items = Invoice.select().where(Invoice.customer.contains(fnd)).order_by(Invoice.customer)
        self.mlb.delete(0,END)
        for p in items:
            self.mlb.insert(END, (p.id,p.customer,p.date,p.amount))
        self.mlb.selection_set(0) #set first row selected

    def btn_del_click(self):
        global admin_login_screen
        global admin_login_entry
        global admin_pwd_entry
        admin_verify = StringVar()
        admin_pwd_verify = StringVar()
        admin_login_screen = Toplevel(self.frame)
        admin_login_screen.title("Admin")
        admin_login_screen.geometry("300x70+500+300")
        admin_login_screen.wm_attributes("-top", 1)
        admin_login_screen.grab_set()
        admin_login_screen.resizable(0,0)
        admin_login_screen.wm_attributes('-fullscreen', False)
        Label( admin_login_screen, text="Password * ").pack()
        admin_pwd_entry = Entry( admin_login_screen, textvariable=admin_pwd_verify, show= '*')
        admin_pwd_entry.pack()
        admin_pwd_entry.focus_set()
        ok = Button(admin_login_screen, text="Ok",command=self.delete)
        ok.pack(side=BOTTOM)
        admin_login_screen.bind("<KeyPress>", self.delete_keypress)

    def delete_keypress(self,event):
        if event.keycode ==13:
            self.delete()
        elif event.keycode ==27:
            admin_login_screen.destroy()

    def delete(self):
        pwd = admin_pwd_entry.get()
        passwords = []; admin = []
        staffss = User.select().where(User.is_admin.contains("yes"))
        for user in staffss: passwords.append(user.password)
        if pwd == '':
            showerror("Error","Password required",parent=admin_login_screen)
        else:
            if any(check_password_hash(passwords[i],pwd)==True for i in range(0,len(passwords))):#pwd in users:
                if self.mlb.item_selected==None:
                    showinfo('info','please select item first',parent=admin_login_screen)
                    admin_login_screen.destroy()
                    return

                admin_login_screen.destroy()
                item = Invoice.get(Invoice.id == self.mlb.item_selected[1])
                msg = messagebox.askquestion('warning','Are you sure you want to delete'+' '+str(self.mlb.item_selected[2]+'?'), icon='warning',parent=self.frame)
                if msg == 'yes':
                    item.delete_instance(recursive=True)
                    self.mlb.delete(self.mlb.item_selected[0])
                    self.mlb.item_selected=None
                else:
                    return
            else:
                showerror("Sorry", "Access denied!\nOnly for admins",parent=admin_login_screen)
        

class FormEditInvoice:
    def __init__(self):
        self.frame=Toplevel()
        self.frame.geometry("500x300+250+200")
        self.frame.wm_attributes("-topmost", 1)
        self.frame.focus_set()
        self.frame.grab_set()
        self.frame1=Frame(self.frame)#,width=100,height=200)
        label_entry(self.frame1,'Invoice#:')
        self.frame1.pack(side=TOP)

        self.frame2=Frame(self.frame)#,width=100,height=200)
        label_entry(self.frame2,'Customer:','Date:')
        self.frame2.pack(side=TOP)

        lblprod=Label(self.frame,text='Items').pack(side=TOP)
        self.frame3=Frame(self.frame)
        self.mlbitems=MultiListbox(self.frame3, (('LN#',5),
                ('Product', 15), ('Quantity',5),('Description', 20),
                ('UnitPrice', 10),('Total',10)))
        self.mlbitems.not_focus() #don't take_focus
        self.mlbitems.pack(expand=YES,fill=BOTH,side=TOP)
        self.frame3.pack(side=TOP)

        self.frame4=Frame(self.frame)#,width=100,height=200)
        label_entry(self.frame4,'GrandTotal:')
        self.frame4.pack(side=TOP)
        self.frame.bind("<Escape>",self.close_form)


    def init_entryboxes(self,val):
        self.frame1._entry.insert(END,val[0])
        self.frame1._entry['state']=DISABLED

        self.frame2._entry.insert(END,val[1])
        self.frame2._entry2.insert(END,val[2])
        self.frame2._entry['state']=DISABLED
        self.frame2._entry2['state']=DISABLED

        self.frame4._entry.insert(END,val[3])
        self.frame4._entry['state']=DISABLED

    def update_mlbitems(self,items):
        self.mlbitems.delete(0,END)
        for i in items:
            qty,price = (i.quantity,i.product.price)
            self.mlbitems.insert(END,(
                i.id,
                i.product.name,
                qty,
                i.product.description,
                price,
                price * qty)
            )
        self.mlbitems.selection_set(0) #set first row selected




    def close_form(self,event):
        #if event.keycode ==27:
        self.frame.destroy()

from __future__ import print_function
from tkinter import *
from tkinter import ttk
from modules.tklistview import MultiListbox
from datetime import datetime
from forms import invoices
from models import Inventory_Product as Product
from models import Inventory_Invoice as Invoice
from models import Inventory_InvoiceItem as InvoiceItem
from tkinter.messagebox import showinfo, askretrycancel
import sys
import nexmo
import random as rand
#import win32print

client = nexmo.Client(key='e9d6bfb6', secret='OUJ8GmGwPRQmnAQ4')
sys.dont_write_bytecode = True

##customer_id = "09DE1769-4B49-449E-92DA-72F2E7AD7B39"
##api_key = "3a0WGzTA6Wa4eGnz80u52LxZleCC7RUChLek1T5ZQuBFGkqZUwyQFTU7ijlJql+l9Y9EMTSi6yJortsxs3/Pdw=="
##phone_number = "+2330555516190"


class FormAddInvoice:
    '''Add New product three labels and three textboxes and an OK button'''
    def __init__(self):
        self.frame=Toplevel()
        self.frame.title('ComStore Pro (Create Invoice)')
        self.frame.geometry("600x600+500+100")
        self.frame.wm_attributes("-topmost", 1)
        self.frame.focus_set()
        self.frame.grab_set()
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()

    def _init_widgets(self):
        global comboPrinter
        self.frame1=Frame(self.frame)
        #invoices.label_entry(self.frame1,'Customer:')
        self.label_cust = Label(self.frame1,text='Customer:')
        self.label_cust.pack(side=LEFT,padx=10)
        self.entry_cust = Entry(self.frame1)
        self.entry_cust.pack(side=LEFT)
        self.customerId = 'RC'+'{:03}'.format(rand.randrange(1, 10**6))
        self.entry_cust.insert(END,self.customerId)
        self.lbl_date=Label(self.frame1,text='Date:'+str(datetime.today())[:10])
        self.lbl_date.pack(side=LEFT,padx=10)
        lblcombo = Label(self.frame1, text = "Choose printer")
        lblcombo.pack(side=LEFT,padx=10)
        #printers = win32print.EnumPrinters(5)
        comboPrinter = ttk.Combobox(self.frame1,values=["First Printer","Second Printer"])
        comboPrinter.pack(side=LEFT,padx=10)
        comboPrinter.current(1)

        self.frame1.pack(side=TOP,anchor=W,pady=10)

        #frame2- lookuplist
        self.frame2=LookupList(self.frame)
        self.frame2.ent.focus() #set_focus to entry product
        self.frame2.ent.bind("<KeyRelease>",self.txtproduct_change)#<Key>",self.keypressed)
        self.frame2.ent.bind("<Return>", lambda e: self.add_item())
        #self.frame2.ent.bind("<Escape>", lambda e: self.ent_paid.focus())#print(e.keycode))#self.ent_qty.focus())
        self.frame.bind("<Escape>", self.close_form)

        #frame3- quantity, ent_qty, btn_additem
        self.frame3=Frame(self.frame)
        self.lbl3_1=Label(self.frame3,text="Quantity")
        self.lbl3_1.pack(side=LEFT)
        self.ent_qty=Entry(self.frame3)
        self.ent_qty.pack(side=LEFT)
        # keyboard events
        self.ent_qty.bind("<Return>", lambda e: self.add_item())

        self.btn_additem=Button(self.frame3,text="Add Item",width=8,
                                command=self.btn_additem_click)
        self.btn_additem.pack(side=LEFT)
        self.btn_clear = Button(self.frame3,text="Clear",width=8, bg="red",
                                command=self.clear)
        self.btn_clear.pack(side=TOP,anchor=W)
        self.frame3.pack(side=TOP,anchor=E)

        #frame4- mlbitems
        self.frame4=Frame(self.frame)
        self.mlbitems=MultiListbox(self.frame4, (('LN#',4),('ID#',6),
                ('Product', 15), ('Quantity',5),('Description', 20),
                ('UnitPrice', 10),('Total',10)))
        #self.mlbitems.not_focus() #don't take_focus
        self.mlbitems.pack(expand=YES,fill=BOTH,side=TOP)
        self.frame4.pack(side=TOP,pady=10)

        #frame5-netamount-stringvar, paid, balance
        self.frame5=Frame(self.frame)
        self.lbl5_1=Label(self.frame5,text="Net:")
        self.lbl5_1.pack(side=LEFT)
        self.netamount=StringVar()
        self.netamount.set('0')
        self.lbl5_2=Label(self.frame5,textvariable=self.netamount, font=("Helvetica", 16))
        self.lbl5_2.pack(side=LEFT)
        self.lbl5_3=Label(self.frame5,text="paid:")
        self.lbl5_3.pack(side=LEFT)
        self.ent_paid=Entry(self.frame5)
        self.ent_paid.pack(side=LEFT)
        self.ent_paid.bind("<KeyPress>",self.ent_paid_change)
        self.ent_paid.bind("<KeyRelease>",self.ent_paid_keyrelease)
        self.balanceamount=StringVar()
        self.lbl5_4=Label(self.frame5,text="Balance: ").pack(side=LEFT)
        self.lblbal=Label(self.frame5,textvariable=self.balanceamount,
                          foreground='red',font=("Helvetica", 22))
        self.lblbal.pack(side=LEFT)

        lbl_ent_paid_help=Label(self.frame5,text="""
            Press <Enter> to create invoice.
            Press <Escape> to close.""")
        lbl_ent_paid_help.pack(side=LEFT)
        self.frame5.pack(side=TOP,anchor=E)

        self.btn_ok=Button(self.frame,text="Add Invoice",width=15,bg="green",command=self.btnok_click)
        self.btn_ok.pack(side=TOP)


    def close_form(self,event):
        if event.keycode==27:
            self.frame.destroy()

    def txtproduct_change(self,event):
        if event.keycode == 77:
            # -> <right arrow key>
            self.ent_qty.focus()
            return
        txtent=self.frame2.ent.get()
        self.frame2.update_mlb(txtent)

    def add_item(self):
        qty=self.ent_qty.get()
        if qty=='':qty=1
        qty=int(qty)
        LN=self.mlbitems.size()+1
        r,i_d,prdct,desc,price=self.frame2.mlb.item_selected
        self.mlbitems.insert(END, (LN,i_d,prdct,qty,desc,price,price*qty))
        net_amt=int(self.netamount.get())+(price*qty)
        self.netamount.set(str(net_amt))# stringvar: change liked to label
        self.frame2.ent.delete(0,END) #clear entry product
        self.ent_qty.delete(0,END)#clear entry quantity
        self.frame2.ent.focus()  #set_focus to entry product
        self.frame2.update_mlb('')

    def ent_paid_change(self,event):
        if event.keycode == 13: # <Enter>
            self.btnok_click()



    def ent_paid_keyrelease(self,event):
        global paid, bal
        paid=self.ent_paid.get()
        if paid=='':paid = 0
        bal=int(paid)-int(self.netamount.get())
        self.balanceamount.set(str(bal))

    def btn_additem_click(self):
        self.add_item()

    def btnok_click(self):
        no_of_items=self.mlbitems.size()
        try:
            if no_of_items==0:
                showinfo("info", "please select some products first!",parent=self.frame)
                return '0'

            global items, all_items
            items=[]; all_items=[]
            for item in range(no_of_items):
                temp1=self.mlbitems.get(item)
                all_items.append((temp1)) # product_id, qty
                items.append((temp1[1],temp1[3])) # product_id, qty
            if self.entry_cust.get() == '':
                showinfo("info", "please provide customer's name or id!",parent=self.frame)
                self.entry_cust.focus()
                #self.frame1._entry.configure(highlightbackground='red', highlightcolor='red')
                return '0'
            if self.ent_paid.get() =='':
                showinfo('Info','Please input money paid',parent=self.frame)
                self.ent_paid.focus()
                return '0'
            cur_inv = Invoice.create(
                customer=self.entry_cust.get(),
                date=str(datetime.today()),
                amount=self.netamount.get()
            )

            for i in items:
                InvoiceItem.insert(
                    invoice=cur_inv,product=i[0],quantity=i[1]).execute()

            self.receipt()
            self.print_receipt()
            self.sendsms()

            self._okbtn_clicked=1
            self.entry_cust.delete(0,END)
            self.ent_paid.delete(0,END)
            self.mlbitems.delete(0,END)
            self.netamount.set('0')
            self.balanceamount.set("")
            self.customer = 'RC'+'{:03}'.format(rand.randrange(1, 10**6))
            self.entry_cust.insert(END,self.customer)
            #self.frame.destroy()
        except:
            pass
    def sendsms(self):
        try:
            # sms for the purchase transaction
            msg = 'Customer with identity' + ' ' + str(self.entry_cust.get()) + ' has purchased items with netamount of ' + ' ' + str(self.netamount.get())
            client.send_message({
                      'from': 'ComStorePro',
                      'to': '+233246746622',
                      'text': msg,
                  })
            client.send_message({
                      'from': 'ComStorePro',
                      'to': '+233241992573',
                      'text': msg,
                  })

            client.send_message({
                      'from': 'ComStorePro',
                      'to': '+233555516190',
                      'text': msg,
                  })
        except:
            showinfo("info","No connection", parent=self.frame)
            pass


    def callback(self):
        self._okbtn_clicked=0
        self.frame.destroy()

    def receipt(self):
        try:
            myFile = open("Receipt.txt","wt")
            myFile.write("\t   COMPUTER SHOP\n    P. O. Box DS 436, Dansoman-Accra\n      Tel: 0555516190/0269381058\n           IBN #:P006762956\n\n")
            myFile.write("To:"+"    "+self.entry_cust.get()+"\nRec #: RC-71-190217\tDate:"+""+str(datetime.today())[:10]+"\n")
            myFile.write("Time:"+""+str(datetime.today())[11:19]+"    Type: CASH\n")
            myFile.write("-"*50+"\n")
            myFile.write("ITEM\t\tQTY\tPRICE\tTOTAL\n")
            myFile.write("-"*50+"\n")

            for i in range(0,len(all_items)):
                myFile.write(str(all_items[i][2])+"\t\t")
                myFile.write(str(all_items[i][3])+"\t")
                myFile.write(str(all_items[i][5])+"\t")
                myFile.write(str(all_items[i][6])+"\n")
            myFile.write("-"*50+"\n")
            myFile.write("\t\tSUBTOTAL: \t"+self.netamount.get()+"\n")
            myFile.write("\t\tDISCOUNT: \t0.00\n")
            myFile.write("\t\tNET TOTAL:\t"+self.netamount.get()+"\n")
            myFile.write("\t\tPAYMENT:\t"+str(paid)+"\n")
            myFile.write("\t\tCHANGE: \t"+str(bal)+"\n")
            myFile.write("-"*50+"\n")
            myFile.write("Cashier:\t"+''+"\tMachine:"+" "+comboPrinter.get()+"\n\n")
            myFile.write("\t3% VAT FLAT RATE ARE ALL INCLUSIVE\n")
            myFile.write("\t      HAVE A NICE DAY!!!\n\n")
            myFile.write("\tSoftware by: Anas Musah\n")
            myFile.write("\t   Tel: +233555516190\n")
            myFile.write("\t Email: bunmalik11@gmail.com")
            myFile.close()
        except:
            pass


    def print_receipt(self):
        try:
            b1 = open("Receipt.txt",'rt').read()
            b = b1.replace(r"\\n\\r",r"\\n")
            if sys.platform=='linux':
               import os
               os.system(comboPrinter.get())
               pass
            elif sys.platform == 'win32':
               import win32print
               printer_name = win32print.GetDefaultPrinter()
               p = win32print.OpenPrinter(printer_name)
               job = win32print.StartDocPrinter(p, 1, ("Receipt", None, "RAW"))
               win32print.StartPagePrinter(p)
               win32print.WritePrinter(p, b)
               win32print.EndPagePrinter(p)
               b1.close()
        except:
            askretrycancel('Retry','check printer',parent=self.frame)
            self.frame.wait_window()
            pass


    def clear(self):
        self.entry_cust.delete(0,END)
        self.ent_paid.delete(0,END)
        self.mlbitems.delete(0,END)
        self.netamount.set('0')
        self.balanceamount.set("")
        self.entry_cust.insert(END,self.customerId)


# LookupList class
# a mlb and a entry box for FormAddInvoice class
class LookupList:
    def __init__(self,master):
        self.frame=Frame(master)#,width=100,height=200)
        self.le_frame=Frame(self.frame)
        lbl=Label(self.le_frame,text="Product: ").pack(side=LEFT)
        self.ent=Entry(self.le_frame)
        self.ent.pack(side=LEFT)
        lbl_produt_help=Label(self.le_frame,text="""
            Press <Enter> to add product with 1 quantity.
            Press <Right Arrow> to get focus to text quantity.
            Press <Escape> to get focus to text paid.""")
        lbl_produt_help.pack(side=LEFT)

        self.le_frame.pack(side=TOP,anchor=W)
        self._init_gridbox()
        self.frame.pack(side=TOP,expand=NO)

    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',5),('Product', 20), ('Description', 32), ('UnitPrice', 15)))
        self.update_mlb('')
        #self.mlb.not_focus()
        self.mlb.pack(expand=YES,fill=BOTH,side=TOP)

    def update_mlb(self,val):
        items = Product.select().where(Product.name.contains(val)).order_by(Product.name)
        self.mlb.delete(0,END)
        for p in items:
            self.mlb.insert(END, (p.id,p.name,p.description,p.price))
        self.mlb.selection_set(0) #set first row selected

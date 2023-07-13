from tkinter import *
from tkinter.ttk import *
from modules.tklistview import MultiListbox
from modules.tktoolbar import _init_toolbar
from models import Inventory_Product as Product
from models import Users as use
from tkinter.messagebox import showinfo
from tkinter import messagebox

class FormProducts:
    '''The Products window with toolbar and a datagrid of products'''
    def __init__(self):
        self.frame=Toplevel()
        self.frame.title('ComStore Pro (Products)')
        self.frame.wm_attributes("-top", 1)
        self.frame.focus_set()
        self.frame.grab_set()
        self.frame.geometry("1000x500+250+200")
        _init_toolbar(self)
        self._init_gridbox()
        self.frm_addproduct=None
        self.frm_editproduct=None
        self.addproductflag=False # frmaddproduct doesn't exist
        self.editproductflag=False

    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',3),('Product', 25), ('Description', 25), ('Price', 10)))
        #tbproducts=sql.session._query("select * from inventory_product")
        #for p in Product.select():print(p.id,p.name)

        self.update_mlb(items=Product.select())
        self.mlb.pack(expand=YES,fill=BOTH)
        self.mlb.focus_set()
        self.frame.bind("<Escape>",self.close_form)
        self.frame.bind("<KeyPress>",self.btn_add_click_keypress)
        self.tb_entryfind.bind("<KeyRelease>",self.tb_btnfind_click)#<Key>",self.keypressed)


    def close_form(self,event):
        #if event.keycode ==27:
        self.frame.destroy()

    # form product add button clicked()
    def btn_add_click(self):
        if self.addproductflag: return 0
        #print ('not exist')
        self.addproductflag=True
        self.frm_addproduct=FormAddProduct()
        self.frame.wait_window(self.frm_addproduct.frame)
        if self.frm_addproduct._okbtn_clicked==1:
            self.update_mlb(Product.select())
        self.addproductflag=False


    def btn_add_click_keypress(self,event):
        if event.keycode == 97:  # <a>
            self.btn_add_click()
        elif event.keycode == 101: # <e>
            self.btn_edit_click()
        elif event.keycode == 100:  # <d>
            self.btn_del_click()

    def btn_edit_click(self):
        if self.editproductflag: return 0
        #print ('not exist')
        self.editproductflag=True
        self.frm_editproduct=FormAddProduct()
        self.frm_editproduct.init_entryboxes(self.mlb.item_selected[1:])#(id,customer,date,amount)
        self.frame.wait_window(self.frm_editproduct.frame)
        item=Product.get(Product.id == self.mlb.item_selected[1])
        if self.frm_editproduct._okbtn_clicked==1:
            self.update_mlbitem(self.mlb.item_selected[0],item)
            item.delete_instance()
        self.editproductflag=False

    def txtproduct_change(self,event):
        if event.keycode == 77:
            # -> <right arrow key>
            self.ent_qty.focus()
            return
        txtent=self.frame2.ent.get()
        self.frame2.update_mlb(txtent)

    def btn_del_click(self):
        if self.mlb.item_selected==None: return showinfo('info','please select item first',parent=self.frame)
        # sql.session._delete_product(int(self.mlb.item_selected[1]))
        item=Product.get(Product.id == self.mlb.item_selected[1])
        msg = messagebox.askquestion('warning','Are you sure you want to delete'+' '+str(self.mlb.item_selected[2]),
		icon='warning',parent=self.frame)
        if msg == 'yes':
            #item.delete_instance()
            self.mlb.delete(self.mlb.item_selected[0])
            self.mlb.item_selected=None
        else:
            return


    def tb_btnfind_click(self,event):
        #self.update_mlb(Product.select().where(Product.name.contains(fnd)))
        self.update_mlbb()

    def update_mlbb(self):
        fnd=self.tb_entryfind.get()
        items = Product.select().where(Product.name.contains(fnd)).order_by(Product.name)
        self.mlb.delete(0,END)
        for p in items:
            self.mlb.insert(END, (p.id,p.name,p.description,p.price))
        self.mlb.selection_set(0) #set first row selected

    def update_mlb(self,items):
        self.mlb.delete(0,END)

        for p in items:
            self.mlb.insert(0, (p.id,p.name,p.description,p.price))
        self.mlb.selection_set(0) #set first row selected

    def update_mlbitem(self,index,item):
        self.mlb.delete(index)
        self.mlb.insert(index, (item.id,item.name,item.description,item.price))
        self.mlb.selection_set(index) #set item edited


class FormAddProduct:
    '''Add New product three labels and three textboxes and an OK button'''
    def __init__(self):

        self.frame=Toplevel()
        #self.frame.geometry("330x100+250+200")
        #self.frame.wm_transient()
        self.frame.wm_attributes("-top", 2)
        self.frame.grab_set()
        self.frame.geometry("330x100+600+400")
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()

    def _init_widgets(self):
        self.label1=Label(self.frame,text="Product #")
        self.label1.grid(row=0,sticky=W)
        self.entry1=Entry(self.frame)
        self.entry1.grid(row=1,column=0)
        self.entry1.focus()

        self.label2=Label(self.frame,text="Sales Price")
        self.label2.grid(row=0,column=1,sticky=W)
        self.entry2=Entry(self.frame)
        self.entry2.grid(row=1,column=1)

        self.label3=Label(self.frame,text="Description.")
        self.label3.grid(row=2,sticky=W,columnspan=2)
        self.entry3=Entry(self.frame)
        self.entry3.grid(row=3,sticky=W+E,columnspan=2)
        self.entry3.bind("<Return>", lambda e: self.btnok_click())

        self.btn_ok=Button(self.frame,text="Add",width=7,command=self.btnok_click)
        self.btn_ok.grid(row=4,column=1,sticky=E)

        self.btn_edit=Button(self.frame,text="Edit",width=7,command=self.btnedit_click)
        self.btn_edit.grid(row=4,column=1)
        #self.frame.bind("<KeyPress>",self.close_form)

    def close_form(self, event):
        if event.keycode==27:
            self.frame.destroy()

    def btnok_click(self):
        items=(self.entry1.get(),self.entry3.get(),self.entry2.get())
        if '' in items:
            showinfo("info", "no item added!",parent=self.frame)
            return 0

        p = Product.create(name=items[0],description=items[1],price=int(items[2]))
        self._okbtn_clicked=1
        showinfo(" ", "item added!",parent=self.frame)
        self.frame.destroy()


    def btnedit_click(self):
        items=(self.entry1.get(),self.entry3.get(),self.entry2.get())
        if '' in items:
            showinfo("info", "no item added!",parent=self.frame)
            return 0

        p = Product.insert(name=items[0],description=items[1],price=int(items[2])).execute()
        self._okbtn_clicked=1
        showinfo(" ", "item edited!", parent=self.frame)
        self.frame.destroy()

    def callback(self):
        self._okbtn_clicked=0
        #print ('user exits the screen')
        self.frame.destroy()

    def init_entryboxes(self,val):
        self.entry3.insert(END,val[2])#description
        self.entry2.insert(END,val[3])#price
        self.entry1.insert(END,val[1])#product name

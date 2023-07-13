#guilistview.py
from tkinter import *
class MultiListbox(Frame):
    '''MultiListbox made by Labels as table header and Listbox as table colomns'''
    def __init__(self, master, lists):
        Frame.__init__(self, master)
        self.lists = []
        self.selection = 0
        for l,w in lists:
            frame = Frame(self); frame.pack(side=LEFT, expand=YES, fill=BOTH)
            Label(frame, text=l, borderwidth=1, relief=RAISED).pack(fill=X)
            lb = Listbox(frame, width=w, borderwidth=0, selectborderwidth=0,
                 relief=FLAT, exportselection=FALSE)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
            lb.bind('<Button-4>', lambda e, s=self: s._scroll(SCROLL, 1, PAGES))
            lb.bind('<Button-5>', lambda e, s=self: s._scroll(SCROLL, -1, PAGES))
        frame = Frame(self); frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[1]['yscrollcommand']=sb.set
        # Configure scrolling by arrow keys and Page Up/Down.
        self.bind_all("<Up>", lambda e, s=self: s._scroll("scroll", "-1", "units", select=True))
        self.bind_all("<Down>", lambda e, s=self: s._scroll("scroll", "1", "units", select=True))
        self.bind_all("<Next>", lambda e, s=self: s._scroll("scroll", "1", "pages", select=True))
        self.bind_all("<Prior>", lambda e, s=self: s._scroll("scroll", "-1", "pages", select=True))


    def _select(self, y):
        row = self.lists[0].nearest(y)
        #logging.info("Selecting Y point %s (got row %s)", y, row)
        return self._select_row(row)

    def _select_row(self, row):
        #logging.info("Selecting row %d", row)
        self.selection_clear(0, END)
        self.selection_set(row)
        # self.see(row)
        return "break"


    def _button2(self, x, y):
        for l in self.lists: l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists: l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            l.yview(*args)
        return 'break'

    def _scroll(self, *args, select=False):
        #select = kwargs.pop("select", False)
        #logging.info("Scrolling -- args: %s, select: %s", args, select)

        if select and self.curselection():
            new_index, should_do_scroll = self.get_new_selection(args)
            if new_index is None:
                #logging.debug("No selection change for args: %s - scrolling...", args)
                should_do_scroll = True
            else:
                old_index = int(self.curselection()[0])
                #logging.debug("Changing selection from index %d to %d", old_index, new_index)
                self._select_row(new_index)
        else:
            should_do_scroll = True

        if should_do_scroll:
            for list_widget in self.lists:
                list_widget.yview(*args)

    def get_new_selection(self, scroll_args):
        """
        If selection change upon scrolling is enabled, return the new index that should be selected after the
        scroll operation finishes. If the new index is currently visible, just select it and skip the actual
        scrolling process entirely.

        :param list scroll_args: The arguments passed to the scrollbar widget
        :return tuple: The index that should be selected afterward, followed by its current "selectability"
        """
        cur_selection = self.curselection()

        # If the scrollbar is being dragged, or if nothing is currently selected, then do not select anything.
        if scroll_args[0] != "scroll" or not cur_selection:
            return None, False
        amount = int(scroll_args[1])
        pixel_dict = self.get_pixel_dict()
        page_size = len(pixel_dict) - 2 if scroll_args[2] == "pages" else 1
        scroll_diff = amount * page_size
        old_index = int(cur_selection[0])
        new_index = max(0, min(self.lists[0].size() - 1, old_index + scroll_diff))
        return new_index, new_index not in pixel_dict

    def get_pixel_dict(self):
        list_box = self.lists[0]
        height = list_box.winfo_height() + 1
        pixel_dict = {list_box.nearest(height): height}
        for pixel in range(height, 0, -1):
            pixel_dict[list_box.nearest(pixel)] = pixel
        max_index, bottom_y = max(pixel_dict.items())
        item_height = bottom_y - pixel_dict.get(max_index - 1, 1)
        while bottom_y + item_height < height:
            max_index += 1
            bottom_y += item_height
            pixel_dict[max_index] = bottom_y
        pixel_dict.pop(max_index)
        return pixel_dict

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        result = []
        for l in self.lists:
            result.append(l.get(first,last))
        if last: return list(map(*[None] + result))
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        self.item_selected=[first,]+self.get(first)
        for l in self.lists:
            l.selection_set(first, last)

    def not_focus(self):#suhail
        for l in self.lists:
            l['takefocus']=False


if __name__ == '__main__':
    tk = Tk()
    Label(tk, text='MultiListbox').pack(side=TOP)
    mlb = MultiListbox(tk, (('Subject', 40), ('Sender', 20), ('Date', 10)))

    for i in range(5000):
        mlb.insert(END, ('Important Message: %d' % i, 'John Doe %d' % i, '10/10/%04d' % (1900+i)))
        mlb.pack(expand=YES,fill=BOTH,side=TOP)
    mlb.selection_set(0)
    print(mlb.item_selected)
    tk.mainloop()

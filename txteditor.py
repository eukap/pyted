from tkinter.filedialog import *
from tkinter import *


class Application(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.menubar = Frame(self)
        self.menubar.config(bg='#444444', bd=0, relief=FLAT)
        self.menubar.pack(side=TOP, fill=X)
        self.toolbar = Frame(self)
        self.toolbar.config(bg='#444444', bd=1, relief=GROOVE, pady=2)
        self.toolbar.pack(side=TOP, fill=X)
        self.text = Text(self)
        self.text.config(fg='#111111', bg='#eeeeee', bd=0, wrap=WORD)
        self.text.focus()
        self.yscroll = Scrollbar(self, orient=VERTICAL)
        self.yscroll.config(cursor='arrow', command=self.text.yview,
                            bg='#5d5d5d', activebackground='#6e6e6e')
        self.text['yscrollcommand'] = self.yscroll.set
        self.yscroll.pack(side=RIGHT, fill=Y)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH)

        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_help_menu()
        self.create_quit_btn()

    def create_file_menu(self):
        menu_btn = Menubutton(self.menubar)
        menu_btn.config(text='File', activebackground='#647899', bg='#444444',
                        underline=0)
        menu_btn.pack(side=LEFT)
        menu_btn.menu = Menu(menu_btn, tearoff=0)
        menu_btn['menu'] = menu_btn.menu
        menu_btn.menu.config(activebackground='#647899', bg='#444444')
        menu_btn.menu.add_command(label='New')
        menu_btn.menu.add_command(label='Open', command=self.open_file)
        menu_btn.menu.add_command(label='Close')
        menu_btn.menu.add_separator()
        menu_btn.menu.add_command(label='Save', command=self.save_file)
        menu_btn.menu.add_command(label='Save As', command=self.save_as_file)
        menu_btn.menu.add_separator()
        menu_btn.menu.add_command(label='Exit', command=exit)

    def open_file(self):
        file = askopenfile()
        if file:
            self.text.delete(1.0, END)
            self.text.insert(1.0, file.read())
            file.close()

    def save_file(self):
        if self.text.edit_modified():
            pass

    def save_as_file(self):
        file = asksaveasfile()
        if file:
            text = self.text.get(1.0, END)
            file.write(text)
            file.close()

    def create_edit_menu(self):
        menu_btn = Menubutton(self.menubar)
        menu_btn.config(text='Edit', activebackground='#647899', bg='#444444',
                        underline=0)
        menu_btn.pack(side=LEFT)
        menu_btn.menu = Menu(menu_btn, tearoff=0)
        menu_btn['menu'] = menu_btn.menu
        menu_btn.menu.config(activebackground='#647899', bg='#444444')
        menu_btn.menu.add_command(label='Undo')
        menu_btn.menu.add_command(label='Redo')
        menu_btn.menu.add_separator()
        menu_btn.menu.add_command(label='Cut', command=self.cut_text)
        menu_btn.menu.add_command(label='Copy', command=self.copy_text)
        menu_btn.menu.add_command(label='Paste', command=self.paste_text)
        menu_btn.menu.add_command(label='Delete', command=self.del_text)
        menu_btn.menu.add_separator()
        menu_btn.menu.add_command(label="Select All", command=self.select_all)

    def cut_text(self):
        try:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.text.clipboard_clear()
            self.text.clipboard_append(text)
        except TclError:
            pass

    def copy_text(self):
        try:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.text.clipboard_clear()
            self.text.clipboard_append(text)
        except TclError:
            pass

    def paste_text(self):
        try:
            text = self.text.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass

    def del_text(self):
        try:
            self.text.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass

    def select_all(self):
        self.text.tag_add(SEL, 1.0, END)

    def create_view_menu(self):
        menu_btn = Menubutton(self.menubar)
        menu_btn.config(text='View', activebackground='#647899', bg='#444444',
                        underline=0)
        menu_btn.pack(side=LEFT)
        menu_btn.menu = Menu(menu_btn, tearoff=0)
        menu_btn['menu'] = menu_btn.menu
        menu_btn.menu.config(activebackground='#647899', bg='#444444')

    def create_help_menu(self):
        menu_btn = Menubutton(self.menubar)
        menu_btn.config(text='Edit', activebackground='#647899', bg='#444444',
                        underline=0)
        menu_btn.pack(side=LEFT)
        menu_btn.menu = Menu(menu_btn, tearoff=0)
        menu_btn['menu'] = menu_btn.menu
        menu_btn.menu.config(activebackground='#647899', bg='#444444')

    def create_quit_btn(self):
        quit_btn = Button(self.toolbar)
        quit_btn.config(text='Quit', font=('Sans', '10'), fg='#eeeeee',
                        bg='#444444', activebackground='#647899', command='exit',
                        bd=1, relief=GROOVE, padx=4, pady=2)
        quit_btn.pack(side=RIGHT)


def main():
    root = Tk()
    root.title('PyTed')
    root.geometry('650x500')
    frame = Application(root)
    frame.pack(side=TOP, expand=YES, fill=BOTH)
    root.mainloop()

    
if __name__ == '__main__':
    main()

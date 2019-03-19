from tkinter.filedialog import *
from tkinter import *
from tkinter.ttk import Notebook, Style
from pathlib import Path


class Application(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        # A list with names of files opened in separate tabs
        self.filenames = ['Untitled']
        # An opened tabs counter
        self.tabcount = 0

        self.menubar = Frame(self)
        self.menubar.config(bg='#444444', bd=0, relief=FLAT)
        self.menubar.pack(side=TOP, fill=X)

        self.toolbar = Frame(self)
        self.toolbar.config(bg='#444444', bd=1, relief=GROOVE, pady=2)
        self.toolbar.pack(side=TOP, fill=X)

        self.style = Style()
        self.style.configure('TNotebook', background='#606060')

        self.notebook = Notebook(self)
        self.notebook.pack(side=TOP, expand=YES, fill=BOTH)

        self.text_frm = Frame(self.notebook)
        self.text_frm.pack(side=TOP, expand=YES, fill=BOTH)

        self.text = Text(self.text_frm)
        self.text.config(fg='#111111', bg='#eeeeee', bd=0, wrap=WORD)
        self.text.focus()
        self.yscroll = Scrollbar(self.text_frm, orient=VERTICAL)
        self.yscroll.config(cursor='arrow', command=self.text.yview,
                            bg='#5d5d5d', activebackground='#6e6e6e')
        self.text['yscrollcommand'] = self.yscroll.set
        self.yscroll.pack(side=RIGHT, fill=Y)
        self.text.pack(side=LEFT, expand=YES, fill=BOTH)

        self.notebook.add(self.text_frm, padding=1,
                          text=self.filenames[self.tabcount])

        self.filemenu = Menubutton(self.menubar)
        self.filemenu.config(text='File', activebackground='#647899',
                             bg='#444444', underline=0)
        self.filemenu.pack(side=LEFT)
        self.filemenu.menu = Menu(self.filemenu, tearoff=0)
        self.filemenu['menu'] = self.filemenu.menu
        self.filemenu.menu.config(activebackground='#647899', bg='#444444')
        self.filemenu.menu.add_command(label='New')
        self.filemenu.menu.add_command(label='Open', command=self.open_file)
        self.filemenu.menu.add_command(label='Close')
        self.filemenu.menu.add_separator()
        self.filemenu.menu.add_command(label='Save', command=self.save_file,
                                       state=DISABLED)
        self.filemenu.menu.add_command(label='Save As',
                                       command=self.save_as_file)
        self.filemenu.menu.add_separator()
        self.filemenu.menu.add_command(label='Exit', command=exit)

        self.editmenu = Menubutton(self.menubar)
        self.editmenu.config(text='Edit', activebackground='#647899',
                             bg='#444444', underline=0)
        self.editmenu.pack(side=LEFT)
        self.editmenu.menu = Menu(self.editmenu, tearoff=0)
        self.editmenu['menu'] = self.editmenu.menu
        self.editmenu.menu.config(activebackground='#647899', bg='#444444')
        self.editmenu.menu.add_command(label='Undo')
        self.editmenu.menu.add_command(label='Redo')
        self.editmenu.menu.add_separator()
        self.editmenu.menu.add_command(label='Cut', command=self.cut_text)
        self.editmenu.menu.add_command(label='Copy', command=self.copy_text)
        self.editmenu.menu.add_command(label='Paste', command=self.paste_text)
        self.editmenu.menu.add_command(label='Delete', command=self.del_text)
        self.editmenu.menu.add_separator()
        self.editmenu.menu.add_command(label="Select All",
                                       command=self.select_all)

        self.viewmenu = Menubutton(self.menubar)
        self.viewmenu.config(text='View', activebackground='#647899',
                             bg='#444444', underline=0)
        self.viewmenu.pack(side=LEFT)
        self.viewmenu.menu = Menu(self.viewmenu, tearoff=0)
        self.viewmenu['menu'] = self.viewmenu.menu
        self.viewmenu.menu.config(activebackground='#647899', bg='#444444')

        self.helpmenu = Menubutton(self.menubar)
        self.helpmenu.config(text='Help', activebackground='#647899',
                             bg='#444444', underline=0)
        self.helpmenu.pack(side=LEFT)
        self.helpmenu.menu = Menu(self.helpmenu, tearoff=0)
        self.helpmenu['menu'] = self.helpmenu.menu
        self.helpmenu.menu.config(activebackground='#647899', bg='#444444')

        self.quit_btn = Button(self.toolbar)
        self.quit_btn.config(text='Quit', font=('Sans', '10'), fg='#eeeeee',
                             bg='#444444', activebackground='#647899',
                             command='exit', bd=1, relief=GROOVE, padx=4,
                             pady=2)
        self.quit_btn.pack(side=RIGHT)

    def open_file(self):
        filepath = askopenfilename()
        if filepath:
            modified = self.text.edit_modified()
            p = Path(filepath)
            filename = p.parts[-1]

            if self.filenames[self.tabcount] == 'Untitled' and not modified:
                self.notebook.hide(self.tabcount)

            self.tabcount += 1
            self.filenames.append(filename)

            self.text_frm = Frame(self.notebook)
            self.text_frm.pack(side=TOP, expand=YES, fill=BOTH)

            self.text = Text(self.text_frm)
            self.text.config(fg='#111111', bg='#eeeeee', bd=0, wrap=WORD)
            self.text.focus()
            self.yscroll = Scrollbar(self.text_frm, orient=VERTICAL)
            self.yscroll.config(cursor='arrow', command=self.text.yview,
                                bg='#5d5d5d', activebackground='#6e6e6e')
            self.text['yscrollcommand'] = self.yscroll.set
            self.yscroll.pack(side=RIGHT, fill=Y)
            self.text.pack(side=LEFT, expand=YES, fill=BOTH)

            self.notebook.add(self.text_frm, padding=1,
                              text=self.filenames[self.tabcount])
            self.notebook.select(self.tabcount)

            file = open(filepath)
            self.text.insert(1.0, file.read())
            file.close()

            self.text.edit_modified(arg=False)

    def save_file(self):
        pass

    def save_as_file(self):
        filepath = asksaveasfilename()
        if filepath:
            text = self.text.get(1.0, END)
            file = open(filepath, 'w')
            file.write(text)
            file.close()

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


def main():
    root = Tk()
    root.title('PyTed')
    root.geometry('650x500')
    frame = Application(root)
    frame.pack(side=TOP, expand=YES, fill=BOTH)
    root.mainloop()


if __name__ == '__main__':
    main()

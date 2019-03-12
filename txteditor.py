from tkinter.filedialog import *
from tkinter import *


<<<<<<< HEAD
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
                        bg='#444444', activebackground='#647899',
                        command='exit', bd=1, relief=GROOVE, padx=4, pady=2)
        quit_btn.pack(side=RIGHT)


def main():
    root = Tk()
    root.title('PyTed')
    root.geometry('650x500')
    frame = Application(root)
    frame.pack(side=TOP, expand=YES, fill=BOTH)
=======
# class MainWindow(Tk):
#     def __init__(self):
#         Tk.__init__(self)
#         self.title('PyTed')
#         self.geometry('650x500+650+280')

class Application(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.config(width=650, height=600)
        # self.menubar_frm = Frame(self)
        # self.menubar_frm.config(bg='#444444')
        # self.menubar_frm.pack(fill=X)
        # self.toolbar_frm = Frame(self)
        # self.menubar_frm.config(bg='#444444')
        # self.toolbar_frm.pack(fill=X)
        self.pack(expand=YES, fill=BOTH)
        self.create_menubar()
        self.create_toolbar()

    def create_menubar(self):
        self.menubar_frm = Frame(self)
        self.menubar_frm.config(bg='#444444')
        self.menubar_frm.pack(fill=X)

    def create_toolbar(self):
        self.toolbar_frm = Frame(self)
        self.toolbar_frm.config(bg='#444444', pady=3, bd=1, relief=GROOVE)
        self.toolbar_frm.pack(fill=X)

    # class TextArea(Text):
    #     def __init__(self, master=None):
    #         Text.__init__(self, master)
    #         master.yscroll = Scrollbar(master, orient=VERTICAL)
    #         master.yscroll.config(cursor='arrow', command=self.yview,
    #                               bg='#5d5d5d', activebackground='#6e6e6e')
    #         self['yscrollcommand'] = master.yscroll.set
    #         master.yscroll.pack(side=RIGHT, fill=Y)
    #         self.config(fg='#111111', bg='#eeeeee', bd=0, wrap=WORD)
    #         self.pack(side=LEFT, expand=YES, fill=BOTH)
    #         self.focus()
    #
    #
    # class FileMenuButton(Menubutton):
    #     def __init__(self, master=None):
    #         Menubutton.__init__(self, master)
    #         self.config(text='File', activebackground='#647899', bg='#444444',
    #                     underline=0)
    #         self.pack(side=LEFT)
    #         self.menu = Menu(self, tearoff=0)
    #         self['menu'] = self.menu
    #         self.menu.config(activebackground='#647899', bg='#444444')
    #         self.menu.add_command(label='New')
    #         self.menu.add_command(label='Open', command=self.open_file)
    #         self.menu.add_command(label='Close')
    #         self.menu.add_separator()
    #         self.menu.add_command(label='Save', command=self.save_file)
    #         self.menu.add_command(label='Save As', command=self.save_as_file)
    #         self.menu.add_separator()
    #         self.menu.add_command(label='Exit', command=exit)
    #
    #     @staticmethod
    #     def open_file():
    #         file = askopenfile()
    #         if file:
    #             Application.text_area.delete(1.0, END)
    #             Application.text_area.insert(1.0, file.read())
    #             file.close()
    #
    #     @staticmethod
    #     def save_file():
    #         if Application.text_area.edit_modified():
    #             pass
    #
    #     @staticmethod
    #     def save_as_file():
    #         file = asksaveasfile()
    #         if file:
    #             text = Application.text_area.get(1.0, END)
    #             file.write(text)
    #             file.close()
    #
    #
    # class EditMenuButton(FileMenuButton):
    #     def __init__(self, master=None):
    #         FileMenuButton.__init__(self, master)
    #         self.config(text='Edit')
    #         self.menu.delete(0, self.menu.index(END))
    #         self.menu.add_command(label='Undo')
    #         self.menu.add_command(label='Redo')
    #         self.menu.add_separator()
    #         self.menu.add_command(label='Cut', command=self.cut_text)
    #         self.menu.add_command(label='Copy', command=self.copy_text)
    #         self.menu.add_command(label='Paste', command=self.paste_text)
    #         self.menu.add_command(label='Delete', command=self.del_text)
    #         self.menu.add_separator()
    #         self.menu.add_command(label="Select All", command=self.select_all)
    #
    #     @staticmethod
    #     def cut_text():
    #         try:
    #             text = Application.text_area.get(SEL_FIRST, SEL_LAST)
    #             Application.text_area.delete(SEL_FIRST, SEL_LAST)
    #             Application.text_area.clipboard_clear()
    #             Application.text_area.clipboard_append(text)
    #         except TclError:
    #             pass
    #
    #     @staticmethod
    #     def copy_text():
    #         try:
    #             text = Application.text_area.get(SEL_FIRST, SEL_LAST)
    #             Application.text_area.clipboard_clear()
    #             Application.text_area.clipboard_append(text)
    #         except TclError:
    #             pass
    #
    #     @staticmethod
    #     def paste_text():
    #         try:
    #             text = Application.text_area.selection_get(selection='CLIPBOARD')
    #             Application.text_area.insert(INSERT, text)
    #         except TclError:
    #             pass
    #
    #     @staticmethod
    #     def del_text():
    #         try:
    #             Application.text_area.delete(SEL_FIRST, SEL_LAST)
    #         except TclError:
    #             pass
    #
    #     @staticmethod
    #     def select_all():
    #         Application.text_area.tag_add(SEL, 1.0, END)
    #
    #
    # class ViewMenuButton(FileMenuButton):
    #     def __init__(self, master=None):
    #         FileMenuButton.__init__(self, master)
    #         self.config(text='View')
    #         self.menu.delete(0, self.menu.index(END))
    #
    #
    # class HelpMenuButton(FileMenuButton):
    #     def __init__(self, master=None):
    #         FileMenuButton.__init__(self, master)
    #         self.config(text='Help')
    #         self.menu.delete(0, self.menu.index(END))
    #
    #
    # class QuitButton(Button):
    #     def __init__(self, master=None):
    #         Button.__init__(self, master)
    #         self.config(text='Quit', font=('Sans', '10'), fg='#eeeeee',
    #                     bg='#444444', activebackground='#647899', command='exit',
    #                     bd=1, relief=GROOVE, padx=4, pady=2)
    #         self.pack(side=RIGHT)


# class Application:
#     mainloop = mainloop
#     window = MainWindow()
#     menu_bar_frm = MenuBarFrame(window)
#     toolbar_frm = ToolbarFrame(window)
#     text_area = TextArea(window)
#     file_menu_btn = FileMenuButton(menu_bar_frm)
#     edit_menu_btn = EditMenuButton(menu_bar_frm)
#     view_menu_btn = ViewMenuButton(menu_bar_frm)
#     help_menu_btn = HelpMenuButton(menu_bar_frm)
#     quit_btn = QuitButton(toolbar_frm)

def main():
    root = Tk()
    frame = Application(root)
>>>>>>> aa715f9c2add6195a060e01a70c880736accc225
    root.mainloop()


if __name__ == '__main__':
    main()

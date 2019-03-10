from tkinter.filedialog import *
from tkinter import *


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
    root.mainloop()


if __name__ == '__main__':
    main()

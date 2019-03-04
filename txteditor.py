from tkinter.filedialog import *
from tkinter import *


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('PyTed')
        self.geometry('650x500+650+280')


class MenuBarFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.config()
        self.pack(fill=X)


class FileMenuButton(Menubutton):
    def __init__(self, master=None):
        Menubutton.__init__(self, master)
        self.config(text='File', activebackground='#647899')
        self.pack(side=LEFT)
        self.menu = Menu(self, tearoff=False)
        self['menu'] = self.menu
        self.menu.config(activebackground='#647899')
        self.menu.add_command(label='Open', command=self.openfile)
        self.menu.add_command(label='Save as', command=self.saveasfile)
        self.menu.add_command(label='Exit', command=exit)

    @staticmethod
    def openfile():
        file = askopenfile()
        if file:
            Application.text_area.insert(1.0, file.read())
            file.close()

    @staticmethod
    def saveasfile():
        file = asksaveasfile()
        if file:
            text = Application.text_area.get(1.0, END)
            file.write(text)
            file.close()


class EditMenuButton(FileMenuButton):
    def __init__(self, master=None):
        FileMenuButton.__init__(self, master)
        self.config(text='Edit')
        # self.pack(side=LEFT)


class ViewMenuButton(FileMenuButton):
    def __init__(self, master=None):
        FileMenuButton.__init__(self, master)
        self.config(text='View')
        # self.pack(side=LEFT)


class HelpMenuButton(FileMenuButton):
    def __init__(self, master=None):
        FileMenuButton.__init__(self, master)
        self.config(text='Help')
        # self.pack(side=LEFT)


class ToolbarFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.config(bg='#444444', pady=3, bd=1, relief=GROOVE)
        self.pack(fill=X)


class QuitButton(Button):
    def __init__(self, master=None):
        Button.__init__(self, master)
        self.config(text='Quit', font=('Sans', '10'), fg='#eeeeee',
                    bg='#444444', activebackground='#647899', command='exit',
                    bd=1, relief=GROOVE, padx=4, pady=2)
        self.pack(side=RIGHT)


class TextArea(Text):
    def __init__(self, master=None):
        Text.__init__(self, master)
        self.config(fg='#111111', bg='#eeeeee')
        self.pack(expand=YES, fill=BOTH)
        self.focus()
        self.scroll_y = Scrollbar(self, orient=VERTICAL)
        self.scroll_y.config(cursor='arrow', command=self.yview, bg='#5d5d5d',
                             activebackground='#6e6e6e')
        self['yscrollcommand'] = self.scroll_y.set
        self.scroll_y.pack(side=RIGHT, fill=Y)


class Application:
    mainloop = mainloop
    window = MainWindow()
    menu_bar_frm = MenuBarFrame(window)
    file_menu_btn = FileMenuButton(menu_bar_frm)
    edit_menu_btn = EditMenuButton(menu_bar_frm)
    view_menu_btn = ViewMenuButton(menu_bar_frm)
    help_menu_btn = HelpMenuButton(menu_bar_frm)
    toolbar_frm = ToolbarFrame(window)
    quit_btn = QuitButton(toolbar_frm)
    text_area = TextArea(window)


if __name__ == '__main__':
    Application.mainloop()

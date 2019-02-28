from tkinter.filedialog import *
from tkinter import *


class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('PyTed')
        self.geometry('600x500+650+280')


class MenuBarFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.config(height=20)
        self.pack(fill=BOTH)


class FileMenuButton(Menubutton):
    def __init__(self, master=None):
        Menubutton.__init__(self, master)
        self.config(text='File')
        self.pack(side=LEFT)
        self.menu = Menu(self)
        self['menu'] = self.menu
        self.menu.add_command(command=self.openfile, label='Open')
        self.menu.add_command(command=asksaveasfilename, label='Save as')
        self.menu.add_command(command=exit, label='Exit')

    @staticmethod
    def openfile():
        filename = askopenfilename()
        file = open(filename, 'r')
        Application.text_area.insert(1.0, file.read())
        file.close()


class EditMenuButton(Menubutton):
    def __init__(self, master=None):
        Menubutton.__init__(self, master)
        self.config(text='Edit')
        self.pack(side=LEFT)


class ViewMenuButton(Menubutton):
    def __init__(self, master=None):
        Menubutton.__init__(self, master)
        self.config(text='View')
        self.pack(side=LEFT)


class HelpMenuButton(Menubutton):
    def __init__(self, master=None):
        Menubutton.__init__(self, master)
        self.config(text='Help')
        self.pack(side=LEFT)


class ToolbarFrame(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.config(bg='#444444', height=30)
        self.pack(fill=BOTH)


class QuitButton(Button):
    def __init__(self, master=None):
        Button.__init__(self, master)
        self.config(text='Quit', fg='#eeeeee', bg='#333333', command='exit')
        self.pack(side=RIGHT)


class TextArea(Text):
    def __init__(self, master=None):
        Text.__init__(self, master)
        self.config(fg='#111111', bg='#eeeeee')
        self.pack(expand=YES, fill=BOTH)
        self.focus()
        self.scroll_y = Scrollbar(self, orient=VERTICAL)
        self.scroll_y.config(cursor='arrow', command=self.yview)
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

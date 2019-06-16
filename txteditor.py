from tkinter.filedialog import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Notebook, Style
from pathlib import Path


class Application(Frame):
    class TextFrameTab:
        def __init__(self, obj):
            self.text_frm = Frame(obj.notebook)
            self.text_frm.pack(side=TOP, expand=YES, fill=BOTH)

            self.text = Text(self.text_frm)
            self.text.config(fg='#111111', bg='#eeeeee', bd=0, wrap=WORD,
                             undo=True, maxundo=50, autoseparators=True)
            self.text.focus()
            self.yscroll = Scrollbar(self.text_frm, orient=VERTICAL)
            self.yscroll.config(cursor='arrow', command=self.text.yview,
                                bg='#5d5d5d', activebackground='#6e6e6e')
            self.text['yscrollcommand'] = self.yscroll.set
            self.yscroll.pack(side=RIGHT, fill=Y)
            self.text.pack(side=LEFT, expand=YES, fill=BOTH)
            self.text.edit_modified(arg=False)

            obj.notebook.add(self.text_frm, padding=1, text=obj.filenames[-1])
            obj.notebook.select(self.text_frm)

            self.file_menu = obj.file_menu
            # Disable 'Save' menu item
            self.file_menu.entryconfigure(4, state=DISABLED)

            self.text.bind('<FocusIn>', self.check_state)
            self.text.bind('<FocusOut>', self.check_state)

        def check_state(self, event):
            event.file_menu = self.file_menu
            modified = self.text.edit_modified()
            if modified:
                # Enable 'Save' menu item
                event.file_menu.entryconfigure(4, state=ACTIVE)
                event.file_menu.entryconfigure(0, state=ACTIVE)
            else:
                event.file_menu.entryconfigure(4, state=DISABLED)

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        # A dictionary with paths to opened and/or saved files
        self.filepaths = {}
        # A list with names of files opened in separate tabs
        self.filenames = ['Untitled']

        self.menubar = Frame(self)
        self.menubar.config(bg='#444444', bd=0, relief=FLAT)
        self.menubar.pack(side=TOP, fill=X)

        self.toolbar = Frame(self)
        self.toolbar.config(bg='#444444', bd=1, relief=GROOVE, pady=2)
        self.toolbar.pack(side=TOP, fill=X)

        self.style = Style()
        self.style.configure('TNotebook', background='#606060')

        self.notebook = Notebook(self)
        self.notebook.enable_traversal()
        self.notebook.pack(side=TOP, expand=YES, fill=BOTH)

        self.file_menubtn = Menubutton(self.menubar)
        self.file_menubtn.config(text='File', bg='#444444', fg='#eeeeee',
                                 activeforeground='#eeeeee',
                                 activebackground='#647899', underline=0)
        self.file_menubtn.pack(side=LEFT)
        self.file_menu = Menu(self.file_menubtn, tearoff=0)
        self.file_menubtn['menu'] = self.file_menu
        self.file_menu.config(fg='#eeeeee', activeforeground='#eeeeee',
                              bg='#444444', activebackground='#647899')
        self.file_menu.add_command(label='New', command=self.create_newdoc)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Close', command=self.close_tab)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_command(label='Save As',
                                   command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=exit)

        self.edit_menubtn = Menubutton(self.menubar)
        self.edit_menubtn.config(text='Edit', fg='#eeeeee', bg='#444444',
                                 activebackground='#647899',
                                 activeforeground='#eeeeee', underline=0)
        self.edit_menubtn.pack(side=LEFT)
        self.edit_menu = Menu(self.edit_menubtn, tearoff=0)
        self.edit_menubtn['menu'] = self.edit_menu
        self.edit_menu.config(fg='#eeeeee', activeforeground='#eeeeee',
                              bg='#444444', activebackground='#647899')
        self.edit_menu.add_command(label='Undo', command=self.undo)
        self.edit_menu.add_command(label='Redo', command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Cut', command=self.cut_text)
        self.edit_menu.add_command(label='Copy', command=self.copy_text)
        self.edit_menu.add_command(label='Paste', command=self.paste_text)
        self.edit_menu.add_command(label='Delete', command=self.del_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Select All',
                                   command=self.select_all)

        self.view_menubtn = Menubutton(self.menubar)
        self.view_menubtn.config(text='View', fg='#eeeeee', bg='#444444',
                                 activeforeground='#eeeeee',
                                 activebackground='#647899', underline=0)
        self.view_menubtn.pack(side=LEFT)
        self.view_menu = Menu(self.view_menubtn, tearoff=0)
        self.view_menubtn['menu'] = self.view_menu
        self.view_menu.config(activebackground='#647899', bg='#444444')

        self.help_menubtn = Menubutton(self.menubar)
        self.help_menubtn.config(text='Help', fg='#eeeeee', bg='#444444',
                                 activeforeground='#eeeeee',
                                 activebackground='#647899', underline=0)
        self.help_menubtn.pack(side=LEFT)
        self.help_menu = Menu(self.help_menubtn, tearoff=0)
        self.help_menubtn['menu'] = self.help_menu
        self.help_menu.config(activebackground='#647899', bg='#444444')

        self.quit_btn = Button(self.toolbar)
        self.quit_btn.config(text='Quit', font=('Sans', '10'), fg='#eeeeee',
                             bg='#444444', activebackground='#647899',
                             activeforeground='#eeeeee', command='exit', bd=0,
                             relief=GROOVE, padx=4, pady=2)
        self.quit_btn.pack(side=RIGHT)

        self.TextFrameTab(self)

    def create_newdoc(self):
        self.filenames.append('Untitled')
        self.TextFrameTab(self)

    def open_file(self):
        filepath = askopenfilename(filetypes=(("All files", "*"), ))
        if filepath:
            p = Path(filepath)
            filename = p.parts[-1]
            try:
                with open(filepath) as file:
                    if (self.notebook.index('end')) > 0:
                        textwidget = self.notebook.focus_get()
                        modified = textwidget.edit_modified()
                        current_index = self.notebook.index('current')
                        self.filepaths[current_index] = filepath

                        if (self.filenames[current_index] == 'Untitled' and
                                not modified):
                            self.filenames[current_index] = filename
                            textwidget.insert(1.0, file.read())
                            textwidget.edit_modified(arg=False)
                            self.notebook.tab('current', text=filename)
                        else:
                            self.filenames.append(filename)
                            tab = self.TextFrameTab(self)
                            tab.text.insert(1.0, file.read())
                            tab.text.edit_modified(arg=False)
                            self.notebook.tab('current', text=filename)
                    else:
                        self.filenames.append(filename)
                        tab = self.TextFrameTab(self)
                        tab.text.insert(1.0, file.read())
                        tab.text.edit_modified(arg=False)
                        self.notebook.tab('current', text=filename)
            except UnicodeDecodeError:
                msg = "'{}' has an incorrect type!".format(filename)
                showerror(message=msg)
                self.close_tab()
                self.create_newdoc()

    def close_tab(self):
        def close(obj):
            try:
                current_index = self.notebook.index('current')
                obj.notebook.forget(current_index)
                del obj.filenames[current_index]

                if current_index in obj.filepaths:
                    del obj.filepaths[current_index]
            except TclError:
                pass

        textwidget = self.focus_lastfor()
        modified = textwidget.edit_modified()
        if modified:
            cur_index = self.notebook.index('current')
            msg = "'{}' has been modified. Do you want " \
                  "to save changes?".format(self.filenames[cur_index])
            msgbox = Message(type=YESNOCANCEL, message=msg, icon=QUESTION)
            answer = msgbox.show()
            if answer == YES:
                self.save_file()
                close(self)
            elif answer == NO:
                close(self)
        else:
            close(self)

    def save_file(self):
        current_index = self.notebook.index('current')
        if current_index in self.filepaths:
            textwidget = self.focus_lastfor()
            text = textwidget.get(1.0, END)
            with open(self.filepaths[current_index], 'w') as file:
                file.write(text)
            self.file_menu.entryconfigure(4, state=DISABLED)
            textwidget.edit_modified(arg=False)
        else:
            self.save_as_file()

    def save_as_file(self):
        filepath = asksaveasfilename()
        if filepath:
            p = Path(filepath)
            filename = p.parts[-1]
            current_index = self.notebook.index('current')
            self.filepaths[current_index] = filepath
            self.notebook.tab('current', text=filename)
            textwidget = self.focus_lastfor()
            text = textwidget.get(1.0, END)
            with open(filepath, 'w') as file:
                file.write(text)
            self.file_menu.entryconfigure(4, state=DISABLED)
            textwidget.edit_modified(arg=False)

    def undo(self):
        textwidget = self.focus_lastfor()
        try:
            textwidget.edit_undo()
        except TclError:
            pass

    def redo(self):
        textwidget = self.focus_lastfor()
        try:
            textwidget.edit_redo()
        except TclError:
            pass

    def cut_text(self):
        textwidget = self.focus_lastfor()
        try:
            text = textwidget.get(SEL_FIRST, SEL_LAST)
            textwidget.delete(SEL_FIRST, SEL_LAST)
            textwidget.clipboard_clear()
            textwidget.clipboard_append(text)
        except TclError:
            pass

    def copy_text(self):
        textwidget = self.focus_lastfor()
        try:
            text = textwidget.get(SEL_FIRST, SEL_LAST)
            textwidget.clipboard_clear()
            textwidget.clipboard_append(text)
        except TclError:
            pass

    def paste_text(self):
        textwidget = self.focus_lastfor()
        try:
            text = textwidget.selection_get(selection='CLIPBOARD')
            textwidget.insert(INSERT, text)
        except TclError:
            pass

    def del_text(self):
        textwidget = self.focus_lastfor()
        try:
            textwidget.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass

    def select_all(self):
        textwidget = self.focus_lastfor()
        textwidget.tag_add(SEL, 1.0, END)


def main():
    root = Tk()
    root.title('PyTed')
    root.geometry('650x500')
    frame = Application(root)
    frame.pack(side=TOP, expand=YES, fill=BOTH)
    root.mainloop()


if __name__ == '__main__':
    main()

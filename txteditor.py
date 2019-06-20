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
            obj.textwidgets.append(self.text)

            obj.notebook.add(self.text_frm, padding=1, text=obj.filenames[-1])
            obj.notebook.select(self.text_frm)

            self.file_menu = obj.file_menu
            self.notebook = obj.notebook
            self.filenames = obj.filenames
            self.save_btn = obj.save_btn

            # Disable 'Save' menu item
            self.file_menu.entryconfigure(4, state=DISABLED)

            self.text.bind('<FocusIn>', self.check_state)
            self.text.bind('<FocusOut>', self.check_state)
            self.text.bind('<Any-Key>', self.check_state)
            self.text.bind('<Any-KeyRelease>', self.check_state)
            self.save_btn.bind('<Motion>', self.check_state)

        def check_state(self, event):
            event.file_menu = self.file_menu
            modified = self.text.edit_modified()
            try:
                current_index = self.notebook.index('current')
                if modified:
                    # Enable 'Save' menu item
                    event.file_menu.entryconfigure(4, state=NORMAL)
                    # Add asterisk to the header of the tab
                    self.notebook.tab(current_index,
                                      text='*'+self.filenames[current_index])
                    self.save_btn.config(state=NORMAL)
                else:
                    # Disable 'Save' menu item
                    event.file_menu.entryconfigure(4, state=DISABLED)
                    # If there is asterisk at the header of the tab,
                    # remove it
                    self.notebook.tab(current_index,
                                      text=self.filenames[current_index])
                    self.save_btn.config(state=DISABLED)
            except TclError:
                pass

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        # A dictionary with paths to opened and/or saved files
        self.filepaths = {}
        # A list with names of files opened in separate tabs
        self.filenames = ['Untitled']
        # A list with existing text widgets
        self.textwidgets = []

        self.menubar = Frame(self)
        self.menubar.config(bg='#444444', bd=0, relief=FLAT, padx=2)
        self.menubar.pack(side=TOP, fill=X)

        self.toolbar = Frame(self)
        self.toolbar.config(bg='#444444', bd=1, relief=GROOVE, pady=6, padx=2)
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
        self.file_menu.add_command(label='Exit', command=self.quit_fromapp)

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

        self.file_tool_frm = Frame(self.toolbar)
        self.file_tool_frm.config(bg='#444444', bd=0, relief=FLAT, padx=4)
        self.file_tool_frm.pack(side=LEFT)

        self.edit_tool_frm = Frame(self.toolbar)
        self.edit_tool_frm.config(bg='#444444', bd=0, relief=FLAT, padx=12)
        self.edit_tool_frm.pack(side=LEFT)

        self.new_btn = Button(self.file_tool_frm)
        self.new_btn.config(text=u'\u2795', font=('Sans', '12'),
                            fg='#eeeeee', bg='#333333', bd=0,
                            relief=FLAT, activebackground='#555555',
                            activeforeground='#ffffff', padx=4, pady=0,
                            command=self.create_newdoc)
        self.new_btn.grid(row=0, column=0)

        self.open_btn = Button(self.file_tool_frm)
        self.open_btn.config(text=u'\u21e9', font=('Sans', '12', 'bold'),
                             fg='#eeeeee', bg='#333333', bd=0,
                             relief=FLAT, activebackground='#555555',
                             activeforeground='#ffffff', padx=4, pady=0,
                             command=self.open_file)
        self.open_btn.grid(row=0, column=1, padx=20)

        self.save_btn = Button(self.file_tool_frm)
        self.save_btn.config(text=u'\u21e7', font=('Sans', '12', 'bold'),
                             fg='#eeeeee', bg='#333333', bd=0,
                             relief=FLAT, activebackground='#555555',
                             activeforeground='#ffffff', padx=4, pady=0,
                             command=self.save_file)
        self.save_btn.grid(row=0, column=2, padx=0)

        self.close_btn = Button(self.file_tool_frm)
        self.close_btn.config(text=u'\u2717', font=('Sans', '12', 'bold'),
                              fg='#eeeeee', bg='#333333', bd=0,
                              relief=FLAT, activebackground='#555555',
                              activeforeground='#ffffff', padx=4, pady=0,
                              command=self.close_tab)
        self.close_btn.grid(row=0, column=3, padx=20)

        self.undo_btn = Button(self.edit_tool_frm)
        self.undo_btn.config(text=u'\u21b6', font=('Sans', '12'),
                             fg='#eeeeee', bg='#333333', bd=0,
                             relief=FLAT, activebackground='#555555',
                             activeforeground='#ffffff', padx=4, pady=0,
                             command=self.undo)
        self.undo_btn.grid(row=0, column=0)

        self.redo_btn = Button(self.edit_tool_frm)
        self.redo_btn.config(text=u'\u21b7', font=('Sans', '12'),
                             fg='#eeeeee', bg='#333333', bd=0,
                             relief=FLAT, activebackground='#555555',
                             activeforeground='#ffffff', padx=4, pady=0,
                             command=self.redo)
        self.redo_btn.grid(row=0, column=1, padx=20)

        self.quit_btn = Button(self.toolbar)
        self.quit_btn.config(text='Quit', font=('Sans', '10'), fg='#eeeeee',
                             bg='#333333', activebackground='#647899',
                             activeforeground='#ffffff', bd=0,  relief=GROOVE,
                             padx=4, pady=2, command=self.quit_fromapp)
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
                    if self.notebook.index('end') > 0:
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
                        self.notebook.tab(0, text=filename)
                        self.filepaths[0] = filepath
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
                del obj.textwidgets[current_index]

                if current_index in obj.filepaths:
                    del obj.filepaths[current_index]
            except TclError:
                pass

        if self.notebook.index('end') > 0:
            textwidget = self.focus_lastfor()
            modified = textwidget.edit_modified()
            if modified:
                curr_index = self.notebook.index('current')
                msg = "'{}' has been modified. Do you want " \
                      "to save changes?".format(self.filenames[curr_index])
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
        if self.notebook.index('end') > 0:
            current_index = self.notebook.index('current')
            if current_index in self.filepaths:
                textwidget = self.focus_get()
                text = textwidget.get(1.0, END)
                with open(self.filepaths[current_index], 'w') as file:
                    file.write(text)
                self.file_menu.entryconfigure(4, state=DISABLED)
                textwidget.edit_modified(arg=False)
            else:
                self.save_as_file()

    def save_as_file(self):
        if self.notebook.index('end') > 0:
            filepath = asksaveasfilename()
            if filepath:
                p = Path(filepath)
                filename = p.parts[-1]
                current_index = self.notebook.index('current')
                self.filepaths[current_index] = filepath
                self.notebook.tab('current', text=filename)
                self.filenames[current_index] = filename
                textwidget = self.focus_get()
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

    def quit_fromapp(self):
        modified = False
        for widget in self.textwidgets:
            if widget.edit_modified():
                modified = True
                break
        if modified:
            msg = "Some changes haven't been saved. " \
                  "Do you really want to exit?"
            msgbox = Message(type=YESNO, message=msg, icon=QUESTION)
            answer = msgbox.show()
            if answer == YES:
                self.quit()
        else:
            self.quit()


def main():
    root = Tk()
    root.title('PyTed')
    root.geometry('650x500')
    frame = Application(root)
    frame.pack(side=TOP, expand=YES, fill=BOTH)
    root.protocol("WM_DELETE_WINDOW", frame.quit_fromapp)
    root.mainloop()


if __name__ == '__main__':
    main()

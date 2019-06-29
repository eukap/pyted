from tkinter.filedialog import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Notebook, Style
from pathlib import Path
import sys
import webbrowser


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
                                bg='#777777', activebackground='#6d6d6d',
                                troughcolor='#c2c2c2')
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

            self.text.bind('<<StateChecking>>', self.check_state)

        def check_state(self, event):
            modified = self.text.edit_modified()
            try:
                current_index = self.notebook.index('current')
                if modified:
                    # Enable 'Save' menu item
                    self.file_menu.entryconfigure(4, state=NORMAL)
                    # Add asterisk to the header of the tab
                    self.notebook.tab(current_index,
                                      text='*' + self.filenames[current_index])
                    self.save_btn.config(state=NORMAL)
                else:
                    # Disable 'Save' menu item
                    self.file_menu.entryconfigure(4, state=DISABLED)
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

        self.statusbar = Frame(self)
        self.statusbar.config(bg='#222222', bd=0, relief=FLAT, padx=20)
        self.statusbar.pack(side=BOTTOM, fill=X)

        self.style = Style()
        self.style.configure('TNotebook', background='#606060')

        self.notebook = Notebook(self)
        self.notebook.enable_traversal()
        self.notebook.pack(side=TOP, expand=YES, fill=BOTH)

        self.file_menu_btn = Menubutton(self.menubar)
        self.file_menu_btn.config(text='File', bg='#444444', fg='#eeeeee',
                                  activeforeground='#eeeeee',
                                  activebackground='#647899', underline=0)
        self.file_menu_btn.pack(side=LEFT)
        self.file_menu = Menu(self.file_menu_btn, tearoff=0)
        self.file_menu_btn['menu'] = self.file_menu
        self.file_menu.config(fg='#eeeeee', activeforeground='#eeeeee',
                              bg='#444444', activebackground='#647899')
        self.file_menu.add_command(label='New', command=self.create_new_doc,
                                   accelerator=' ' * 14 + 'Ctrl+N')
        self.file_menu.add_command(label='Open', command=self.open_file,
                                   accelerator=' ' * 14 + 'Ctrl+O')
        self.file_menu.add_command(label='Close', command=self.close_tab,
                                   accelerator=' ' * 14 + 'Ctrl+W')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save', command=self.save_file,
                                   accelerator=' ' * 14 + 'Ctrl+S')
        self.file_menu.add_command(label='Save As', command=self.save_as_file,
                                   accelerator='    Ctrl+Shift+S')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.quit_from_app,
                                   accelerator=' ' * 14 + 'Ctrl+Q')

        self.edit_menu_btn = Menubutton(self.menubar)
        self.edit_menu_btn.config(text='Edit', fg='#eeeeee', bg='#444444',
                                  activebackground='#647899',
                                  activeforeground='#eeeeee', underline=0)
        self.edit_menu_btn.pack(side=LEFT)
        self.edit_menu = Menu(self.edit_menu_btn, tearoff=0)
        self.edit_menu_btn['menu'] = self.edit_menu
        self.edit_menu.config(fg='#eeeeee', activeforeground='#eeeeee',
                              bg='#444444', activebackground='#647899')
        self.edit_menu.add_command(label='Undo', command=self.undo,
                                   accelerator=' ' * 10 + 'Ctrl+Z')
        self.edit_menu.add_command(label='Redo', command=self.redo,
                                   accelerator='Ctrl+Shift+Z')
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Cut', command=self.cut_text,
                                   accelerator=' ' * 10 + 'Ctrl+X')
        self.edit_menu.add_command(label='Copy', command=self.copy_text,
                                   accelerator=' ' * 10 + 'Ctrl+C')
        self.edit_menu.add_command(label='Paste', command=self.paste_text,
                                   accelerator=' ' * 10 + 'Ctrl+V')
        self.edit_menu.add_command(label='Delete', command=self.del_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Select All', command=self.select_all,
                                   accelerator=' ' * 10 + 'Ctrl+A')

        self.help_menu_btn = Menubutton(self.menubar)
        self.help_menu_btn.config(text='Help', fg='#eeeeee', bg='#444444',
                                  activeforeground='#eeeeee',
                                  activebackground='#647899', underline=0)
        self.help_menu_btn.pack(side=LEFT)
        self.help_menu = Menu(self.help_menu_btn, tearoff=0)
        self.help_menu_btn['menu'] = self.help_menu
        self.help_menu.config(fg='#eeeeee', activeforeground='#eeeeee',
                              bg='#444444', activebackground='#647899')
        self.help_menu.add_command(label='About', command=self.show_about)

        self.file_tool_frm = Frame(self.toolbar)
        self.file_tool_frm.config(bg='#444444', bd=0, relief=FLAT, padx=4)
        self.file_tool_frm.pack(side=LEFT)

        self.edit_tool_frm = Frame(self.toolbar)
        self.edit_tool_frm.config(bg='#444444', bd=0, relief=FLAT, padx=12)
        self.edit_tool_frm.pack(side=LEFT)

        self.hint_lbl = Label(self.toolbar)
        self.hint_lbl.config(bg='#444444', fg='#eeeeee',
                             font=('Sans', '10', 'italic'),
                             bd=0, relief=FLAT, padx=12)
        self.hint_lbl.pack(side=LEFT)

        self.new_btn = Button(self.file_tool_frm)
        self.new_btn.config(text='\u2795', font=('Sans', '12'),
                            fg='#eeeeee', bg='#333333', bd=0,
                            relief=FLAT, activebackground='#555555',
                            activeforeground='#ffffff', padx=4, pady=0,
                            command=self.create_new_doc)
        self.new_btn.grid(row=0, column=0)
        self.new_btn.bind('<Enter>',
                          lambda x: self.hint_lbl.config(text='New'))
        self.new_btn.bind('<Leave>', lambda x: self.hint_lbl.config(text=''))

        self.open_btn = Button(self.file_tool_frm)
        self.open_btn.config(text='\u21e9', font=('Sans', '12', 'bold'),
                             fg='#eeeeee', bg='#333333', bd=0,
                             relief=FLAT, activebackground='#555555',
                             activeforeground='#ffffff', padx=4, pady=0,
                             command=self.open_file)
        self.open_btn.grid(row=0, column=1, padx=20)
        self.open_btn.bind('<Enter>',
                           lambda x: self.hint_lbl.config(text='Open'))
        self.open_btn.bind('<Leave>', lambda x: self.hint_lbl.config(text=''))

        self.save_btn = Button(self.file_tool_frm)
        self.save_btn.config(text='\u21e7', font=('Sans', '12', 'bold'),
                             fg='#eeeeee', bg='#333333', bd=0,
                             relief=FLAT, activebackground='#555555',
                             activeforeground='#ffffff', padx=4, pady=0,
                             state=DISABLED, command=self.save_file)
        self.save_btn.grid(row=0, column=2, padx=0)
        self.save_btn.bind('<Enter>',
                           lambda x: self.hint_lbl.config(text='Save'))
        self.save_btn.bind('<Leave>', lambda x: self.hint_lbl.config(text=''))
        self.save_btn.bind('<Motion>', self.save_btn_handler)

        self.close_btn = Button(self.file_tool_frm)
        self.close_btn.config(text='\u2717', font=('Sans', '12', 'bold'),
                              fg='#eeeeee', bg='#333333', bd=0,
                              relief=FLAT, activebackground='#555555',
                              activeforeground='#ffffff', padx=4, pady=0,
                              command=self.close_tab)
        self.close_btn.grid(row=0, column=3, padx=20)
        self.close_btn.bind('<Enter>',
                            lambda x: self.hint_lbl.config(text='Close'))
        self.close_btn.bind('<Leave>', lambda x: self.hint_lbl.config(text=''))

        self.undo_btn = Button(self.edit_tool_frm)
        self.undo_btn.config(text='\u21b6', font=('Sans', '12'),
                             fg='#eeeeee', bg='#333333', bd=0,
                             relief=FLAT, activebackground='#555555',
                             activeforeground='#ffffff', padx=4, pady=0,
                             command=self.undo)
        self.undo_btn.grid(row=0, column=0)
        self.undo_btn.bind('<Enter>',
                           lambda x: self.hint_lbl.config(text='Undo'))
        self.undo_btn.bind('<Leave>', lambda x: self.hint_lbl.config(text=''))

        self.redo_btn = Button(self.edit_tool_frm)
        self.redo_btn.config(text='\u21b7', font=('Sans', '12'),
                             fg='#eeeeee', bg='#333333', bd=0,
                             relief=FLAT, activebackground='#555555',
                             activeforeground='#ffffff', padx=4, pady=0,
                             command=self.redo)
        self.redo_btn.grid(row=0, column=1, padx=20)
        self.redo_btn.bind('<Enter>',
                           lambda x: self.hint_lbl.config(text='Redo'))
        self.redo_btn.bind('<Leave>', lambda x: self.hint_lbl.config(text=''))

        self.quit_btn = Button(self.toolbar)
        self.quit_btn.config(text='Quit', font=('Sans', '10'), fg='#eeeeee',
                             bg='#333333', activebackground='#647899',
                             activeforeground='#ffffff', bd=0,  relief=GROOVE,
                             padx=4, pady=2, command=self.quit_from_app)
        self.quit_btn.pack(side=RIGHT)

        self.TextFrameTab(self)

        self.statusbar_lbl = Label(self.statusbar)
        self.statusbar_lbl.config(text='column:', fg='#ffffff', bg='#222222',
                                  activeforeground='#ffffff',
                                  activebackground='#222222', bd=0,
                                  font=('Sans', '11', 'italic'), padx=40)
        self.statusbar_lbl.pack(side=RIGHT)

        self.statusbar_lbl = Label(self.statusbar)
        self.statusbar_lbl.config(text='line:', fg='#ffffff', bg='#222222',
                                  activeforeground='#ffffff',
                                  activebackground='#222222', bd=0,
                                  font=('Sans', '11', 'italic'), padx=0)
        self.statusbar_lbl.pack(side=RIGHT)

        # Create event bindings for keyboard shortcuts
        self.bind_all('<Control-n>', self.create_new_doc)
        self.bind_all('<Control-o>', self.open_file)
        self.bind_all('<Control-w>', self.close_tab)
        self.bind_all('<Control-s>', self.save_file)
        self.bind_all('<Control-Shift-S>', self.save_as_file)
        self.bind_all('<Control-q>', self.quit_from_app)
        self.bind_all('<Control-a>', self.select_all)
        if sys.platform.startswith('win32'):
            self.bind_all('<Control-Shift-Z>', self.redo)

        # Create the '<<StateChecking>>' virtual event
        self.event_add('<<StateChecking>>', '<Any-KeyPress>',
                       '<Any-KeyRelease>', '<Any-ButtonRelease>',
                       '<FocusIn>', '<FocusOut>')

    def save_btn_handler(self, event):
        try:
            textwidget = self.focus_lastfor()
            current_index = self.notebook.index('current')
            if textwidget.edit_modified():
                self.save_btn.config(state=NORMAL)
                # Add asterisk to the header of the tab
                self.notebook.tab(current_index,
                                  text='*' + self.filenames[current_index])
            else:
                self.save_btn.config(state=DISABLED)
                # If there is asterisk at the header of the tab,
                # remove it
                self.notebook.tab(current_index,
                                  text=self.filenames[current_index])
        except TclError:
            pass

    def create_new_doc(self, *event):
        # event is the '<Control-n>' probable event
        self.filenames.append('Untitled')
        self.TextFrameTab(self)

    def open_file(self, *event):
        # If there is the '<Control-o>' event
        if event:
            textwidget = self.focus_lastfor()
            textwidget.edit_modified(arg=False)
        filepath = askopenfilename(filetypes=(('All files', '*'), ))
        if filepath:
            p = Path(filepath)
            filename = p.parts[-1]
            try:
                with open(filepath) as file:
                    if self.notebook.index('end') > 0:
                        textwidget = self.focus_lastfor()
                        modified = textwidget.edit_modified()
                        current_index = self.notebook.index('current')
                        if (self.filenames[current_index] == 'Untitled' and
                                not modified):
                            self.filepaths[current_index] = filepath
                            self.filenames[current_index] = filename
                            textwidget.insert(1.0, file.read())
                            textwidget.edit_modified(arg=False)
                            self.notebook.tab('current', text=filename)
                        else:
                            self.filepaths[current_index + 1] = filepath
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
                msg = "Unknown encoding!".format(filename)
                showerror(message=msg)
                self.close_tab()
                self.create_new_doc()

    def close_tab(self, *event):
        # event is the '<Control-w>' probable event
        def close(obj):
            try:
                current_index = self.notebook.index('current')
                del obj.filenames[current_index]
                del obj.textwidgets[current_index]
                if current_index in obj.filepaths:
                    del obj.filepaths[current_index]

                obj.notebook.forget(current_index)

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

    def save_file(self, *event):
        # event is the '<Control-s>' probable event
        if self.notebook.index('end') > 0:
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

    def save_as_file(self, *event):
        # event is the '<Control-Shift-S>' probable event
        if self.notebook.index('end') > 0:
            filepath = asksaveasfilename()
            if filepath:
                p = Path(filepath)
                filename = p.parts[-1]
                current_index = self.notebook.index('current')
                self.filepaths[current_index] = filepath
                self.notebook.tab('current', text=filename)
                self.filenames[current_index] = filename
                textwidget = self.focus_lastfor()
                text = textwidget.get(1.0, END)
                with open(filepath, 'w') as file:
                    file.write(text)
                self.file_menu.entryconfigure(4, state=DISABLED)
                textwidget.edit_modified(arg=False)

    def undo(self):
        try:
            textwidget = self.focus_lastfor()
            textwidget.edit_undo()
        except TclError:
            pass

    def redo(self, *event):
        # event is the '<Control-Shift-Z>' probable event for Windows
        try:
            textwidget = self.focus_lastfor()
            textwidget.edit_redo()
        except TclError:
            pass

    def cut_text(self):
        try:
            textwidget = self.focus_lastfor()
            text = textwidget.get(SEL_FIRST, SEL_LAST)
            textwidget.delete(SEL_FIRST, SEL_LAST)
            textwidget.clipboard_clear()
            textwidget.clipboard_append(text)
        except TclError:
            pass

    def copy_text(self):
        try:
            textwidget = self.focus_lastfor()
            text = textwidget.get(SEL_FIRST, SEL_LAST)
            textwidget.clipboard_clear()
            textwidget.clipboard_append(text)
        except TclError:
            pass

    def paste_text(self):
        try:
            textwidget = self.focus_lastfor()
            text = textwidget.selection_get(selection='CLIPBOARD')
            textwidget.insert(INSERT, text)
        except TclError:
            pass

    def del_text(self):
        try:
            textwidget = self.focus_lastfor()
            textwidget.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass

    def select_all(self, *event):
        # event is the '<Control-a>' probable event
        textwidget = self.focus_lastfor()
        textwidget.tag_add(SEL, 1.0, END)

    def show_about(self):
        txt_0 = "PyTEd 0.1.0"
        txt_1 = "PyTEd is a simple text editor based\n" \
                "on the tkinter interface"
        txt_2 = "Copyright " + '\u00a9' + " 2019 Eugene Kapshuk"
        txt_3 = "Source code: "
        txt_4 = "https://github.com/eukap/pyted"
        txt_5 = "License: MIT"
        window = Toplevel()
        window.title('About PyTEd')
        window.geometry('350x280')
        window.transient(self)
        window.resizable(width=False, height=False)

        label_0 = Label(window)
        label_0.config(fg='#000000', bg='#ddddd8', text=txt_0,
                       font=('Sans', '12', 'bold'),
                       justify=CENTER, pady=10)
        label_0.pack(side=TOP, fill=X)

        label_1 = Label(window)
        label_1.config(fg='#000000', bg='#ddddd8', text=txt_1,
                       font=('Sans', '11', 'normal'),
                       justify=CENTER, pady=10)
        label_1.pack(side=TOP, fill=X)

        label_2 = Label(window)
        label_2.config(fg='#000000', bg='#ddddd8', text=txt_2,
                       font=('Sans', '11', 'normal'),
                       justify=CENTER, pady=10)
        label_2.pack(side=TOP, fill=X)

        frame_0 = Frame(window)
        frame_0.config(bg='#ddddd8', bd=0, relief=FLAT, padx=2, pady=2)
        frame_0.pack(side=TOP, fill=X)

        label_3 = Label(frame_0)
        label_3.config(fg='#000000', bg='#ddddd8', text=txt_3,
                       font=('Sans', '11', 'normal'),
                       justify=CENTER, padx=2, pady=10)
        label_3.pack(side=LEFT, fill=X)

        label_4 = Label(frame_0)
        label_4.config(fg='#1111cc', bg='#ddddd8', text=txt_4,
                       font=('Sans', '11', 'normal'), cursor='hand1',
                       justify=CENTER, padx=4, pady=0)
        label_4.pack(side=LEFT, fill=X)
        label_4.bind('<Button-1>', lambda x: webbrowser.open_new_tab(
            'https://github.com/eukap/pyted'))

        label_5 = Label(window)
        label_5.config(fg='#000000', bg='#ddddd8', text=txt_5,
                       font=('Sans', '11', 'normal'),
                       justify=CENTER, pady=8)
        label_5.pack(side=TOP, fill=X)

        frame_1 = Frame(window)
        frame_1.config(bg='#ddddd8', bd=0, relief=FLAT, padx=0, pady=12)
        frame_1.pack(side=BOTTOM, fill=BOTH, expand=YES)

        btn = Button(frame_1)
        btn.config(text='Close', fg='#000000', bg='#efefef',
                   activeforeground='#000000',
                   activebackground='#e9e9e9',
                   font=('Sans', '10', 'normal'), command=window.destroy)
        btn.pack(side=TOP)

    def quit_from_app(self, *event):
        # event is the '<Control-q>' probable event
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
    root.protocol('WM_DELETE_WINDOW', frame.quit_from_app)
    root.mainloop()


if __name__ == '__main__':
    main()

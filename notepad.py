from tkinter import *
from tkinter import filedialog,colorchooser,messagebox

class Notepad:

    current_file="no_file"
    def clear(self,event=""):
        self.txt_area.delete(1.0, END)
    def new_file(self):
        s = self.txt_area.get(1.0, END)
        # print("a=",s)
        if not s.strip():
            pass
        else:
            result = messagebox.askyesnocancel("Save Dialog box", "Do you want to save this file?")
            if result == True:
                self.saveas_file()
                self.clear()
            elif result == False:
                self.clear()
    def open_file(self):
        result = filedialog.askopenfile(initialdir="/", title="Select To openfile",
                                        filetypes=(("Text FILE", "*.txt"), ("ALL FILE", "*.*")))

        # to print the text of file
        for data in result:
            self.txt_area.insert(INSERT, data)
        self.current_file=result.name
        print(self.current_file)
    def save_file(self):
        if self.current_file == "no_file":
            self.saveas_file()
        else:
            f = open(self.current_file, mode="w")
            f.write(self.txt_area.get(1.0, END))
            f.close()
    def saveas_file(self):
        save=filedialog.asksaveasfile(mode="w",defaultextension="*.txt")
        data = self.txt_area.get(1.0, END)
        save.write(data)
        self.current_file = save.name
        print(self.current_file)
    def exit_file(self):
        s = self.txt_area.get(1.0, END)
        # print("a=",s)
        if not s.strip():
            quit()
        else:
            result = messagebox.askyesnocancel("Save Dialog box", "Do you want to save this file?")
            if result == True:
                self.saveas_file()
            elif result == False:
                quit()

    def cut_file(self):
        self.copy_file()
        self.txt_area.delete('sel.first', 'sel.last')

    def copy_file(self):
        self.txt_area.clipboard_clear()
        self.txt_area.clipboard_append(self.txt_area.selection_get())
    def paste_file(self):
        self.txt_area.insert(INSERT, self.txt_area.clipboard_get())
    def del_file(self):
        self.txt_area.delete('sel.first', 'sel.last')

    def change_color(self):
        c = colorchooser.askcolor()
        self.txt_area.configure(background=c[1])
    def change_fore_color(self):
        c = colorchooser.askcolor()
        self.txt_area.configure(foreground=c[1])
    def __init__(self,master):
       self.txt_area = Text(master,  padx=5, pady=5, wrap=WORD, selectbackground="red",
                            bd=2, insertwidth=3,undo=True)
       master.bind("<Control-d>",self.clear)
       master.bind("<Control-D>", self.clear)
       self.txt_area.pack(fill=BOTH, expand=1)
       self.master=master

       self.main_menu = Menu()
       self.master.config(menu=self.main_menu)
       # creating file menu
       self.file_menu = Menu(self.main_menu, tearoff=False)
       self.main_menu.add_cascade(label="File ", menu=self.file_menu)
       self.file_menu.add_command(label="New", command=self.new_file,accelerator="Ctrl+N")
       # to add open in file menu
       self.file_menu.add_command(label="Open",command=self.open_file)
       self.file_menu.add_separator()
       self.file_menu.add_command(label="Save",command=self.save_file)
       self.file_menu.add_command(label="SaveAs",command=self.saveas_file)
       self.file_menu.add_command(label="Exit", command=self.exit_file)
       # seprator
       # creating Edit menu
       self.edit_menu = Menu(self.main_menu, tearoff=False)
       self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
       # to add menu in edit menu
       self.edit_menu.add_command(label="Undo", command=self.txt_area.edit_undo)
       self.edit_menu.add_command(label="Redo", command=self.txt_area.edit_redo)
       self.edit_menu.add_separator()
       self.edit_menu.add_command(label="Cut", command=self.cut_file)
       self.edit_menu.add_command(label="Copy", command=self.copy_file)
       self.edit_menu.add_command(label="Paste", command=self.paste_file)
       self.edit_menu.add_command(label="Delete     Ctrl+d", command=self.del_file)
       self.edit_menu.add_separator()

       # creating Color menu
       self.color_menu = Menu(self.main_menu, tearoff=False)
       self.main_menu.add_cascade(label="Format", menu=self.color_menu)
       # to add menu in format menu
       self.color_menu.add_command(label="BackGround color", command=self.change_color)
       self.color_menu.add_command(label="ForeGround color", command=self.change_fore_color)


root=Tk()
b=Notepad(root)




mainloop()
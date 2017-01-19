import os
import tkinter as tk
from functools import partial
from tkinter import filedialog

import directory_tree_lister


class Application(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self) -> None:
        # Choose a directory button
        self.ask_dir = tk.Button(self, text='Choose a directory', command=self.askdirectory)
        self.ask_dir.pack(side='top')

        # Text button
        self.make_list_text = tk.Button(self, text="Create Text File Directory Tree", state='disabled')
        self.make_list_text.pack(side='top')

        # Excel button
        self.make_list_excel = tk.Button(self, text="Create Excel File Directory Tree", state='disabled')
        self.make_list_excel.pack(side='top')

        # Quit button
        self.quit = tk.Button(self, text="Quit", command=root.destroy)
        self.quit.pack(side='top')

        # Selected directory Label
        self.selected_dir = tk.Label(self.master, text='', wraplength=375)
        self.selected_dir.pack(side='top')

        # Output Label
        self.output = tk.Label(self.master, text='', wraplength=375)
        self.output.pack(side='top')

    def askdirectory(self) -> None:
        self.dirname = tk.filedialog.askdirectory(initialdir='.')

        if self.dirname:
            self.selected_dir.config(text='Directory: {}'.format(self.dirname))

            self.make_list_text.config(state='active', command=partial(self.make_dir_tree_excel, self.dirname))
            self.make_list_excel.config(state='active', command=partial(self.make_dir_tree_text, self.dirname))

    def make_dir_tree_excel(self, directory: str) -> None:
        directory_tree_lister.list_directory_tree_excel(directory)

        file_name = directory.split('/')[-1]
        output_file = '{path}/{file}'.format(path=os.path.dirname(os.path.abspath(__file__)),
                                             file='directory-tree-{}.xlsx'.format(file_name))

        self.output.config(text='Created excel file: {}'.format(output_file))

    def make_dir_tree_text(self, directory: str) -> None:
        directory_tree_lister.list_directory_tree_text(directory)

        file_name = directory.split('/')[-1]
        output_file = '{path}/{file}'.format(path=os.path.dirname(os.path.abspath(__file__)),
                                             file='directory-tree-{}.txt'.format(file_name))

        self.output.config(text='Created text file: {}'.format(output_file))


# create the application
root = tk.Tk()
app = Application(master=root)

# Title and sizing
app.master.title('Directory Tree Lister')
app.master.minsize(400, 220)
app.master.maxsize(400, 220)
app.master.resizable(False, False)

# start the program
app.mainloop()

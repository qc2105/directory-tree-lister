import os
import tkinter as tk
from functools import partial
from tkinter import filedialog

import directory_tree_lister


class Application(tk.Frame):
    """
    Class for Directory Tree Lister GUI methods.
    """

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Creates Buttons and Labels.
        """
        # Choose a directory button
        self.ask_dir_btn = tk.Button(self, text='Choose a directory', command=self.ask_directory)
        self.ask_dir_btn.pack()

        # Text button
        self.make_list_text_btn = tk.Button(self, text="Create Text File Directory Tree", state='disabled')
        self.make_list_text_btn.pack()

        # Excel button
        self.make_list_excel_btn = tk.Button(self, text="Create Excel File Directory Tree", state='disabled')
        self.make_list_excel_btn.pack()

        # Quit button
        self.quit_btn = tk.Button(self, text="Quit", command=root.destroy)
        self.quit_btn.pack()

        # Selected directory Label
        self.selected_dir_label = tk.Label(self.master, text='', justify='left', wraplength=375)
        self.selected_dir_label.pack()

        # Output Label
        self.output_label = tk.Label(self.master, text='', justify='left', wraplength=375)
        self.output_label.pack()

    def ask_directory(self) -> None:
        """
        Creates a file dialog and enables and loads methods into Make List buttons.
        """
        # Ask directory
        self.dirname = tk.filedialog.askdirectory(initialdir='.')

        if self.dirname:
            # Outputs message of selected directory to GUI
            self.selected_dir_label.config(text='Directory:\n{}'.format(self.dirname))

            # Make buttons active
            self.make_list_text_btn.config(state='active', command=partial(self.make_dir_tree_excel, self.dirname))
            self.make_list_excel_btn.config(state='active', command=partial(self.make_dir_tree_text, self.dirname))

    def make_dir_tree_excel(self, directory: str) -> None:
        """
        Creates a xlsx file of a Directory Tree, and outputs message to 'output' Label.

        :param directory: a directory string
        :type directory: str
        """
        directory_tree_lister.list_directory_tree_excel(directory)

        file_name = directory.split('/')[-1]

        output_file_location = '{path}/{file}'.format(
            path=os.path.dirname(os.path.abspath(__file__)),
            file='directory-tree-{}.xlsx'.format(file_name)
        )

        # Outputs message of file created to GUI
        self.output_label.config(text='Created excel file:\n{}'.format(output_file_location))

    def make_dir_tree_text(self, directory: str) -> None:
        """
        Creates a txt file of a Directory Tree, and outputs message to 'output' Label.

        :param directory: a directory string
        :type directory: str
        """
        directory_tree_lister.list_directory_tree_text(directory)

        file_name = directory.split('/')[-1]

        output_file_location = '{path}/{file}'.format(
            path=os.path.dirname(os.path.abspath(__file__)),
            file='directory-tree-{}.txt'.format(file_name)
        )

        # Outputs message of file created to GUI
        self.output_label.config(text='Created text file:\n{}'.format(output_file_location))


if __name__ == '__main__':
    # create the application
    root = tk.Tk()
    app = Application(master=root)

    # Title and sizing
    app.master.title('Directory Tree Lister')
    app.master.minsize(400, 250)
    app.master.maxsize(400, 250)
    app.master.resizable(False, False)

    # start the program
    app.mainloop()

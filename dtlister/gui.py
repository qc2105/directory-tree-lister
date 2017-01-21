import sys
import tkinter as tk
from functools import partial
from tkinter import filedialog

from dtlister import core


class Application(tk.Frame):
    """
    Class consisting of Directory Tree Lister GUI methods.
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
        self.ask_dir_btn = tk.Button(self, text='Choose a directory to scan', command=self.ask_directory)
        self.ask_dir_btn.pack()

        # Choose a output directory button
        self.ask_output_dir_btn = tk.Button(self, text='Choose an output directory', command=self.ask_output_directory,
                                            state='disabled')
        self.ask_output_dir_btn.pack()

        # Text button
        self.make_list_text_btn = tk.Button(self, text="Create Text File Directory Tree", state='disabled')
        self.make_list_text_btn.pack()

        # Excel button
        self.make_list_excel_btn = tk.Button(self, text="Create Excel File Directory Tree", state='disabled')
        self.make_list_excel_btn.pack()

        # Quit button
        self.quit_btn = tk.Button(self, text="Quit", command=root.destroy)
        self.quit_btn.pack()

        # Selected directory label
        self.selected_dir_label = tk.Label(self.master, text='', justify='left', wraplength=375)
        self.selected_dir_label.pack()

        # Selected output directory label
        self.selected_output_dir_label = tk.Label(self.master, text='', justify='left', wraplength=375)
        self.selected_output_dir_label.pack()

        # Output label
        self.output_label = tk.Label(self.master, text='', justify='left', wraplength=375)
        self.output_label.pack()

    def ask_directory(self) -> None:
        """
        Creates a file dialog and outputs select directory value to label.
        """
        # Ask user for directory
        self.dirname = tk.filedialog.askdirectory()

        if self.dirname:
            # Outputs message of selected directory to GUI
            self.selected_dir_label.config(text='Scan Directory:\n{}'.format(self.dirname))

            # Make button active
            self.ask_output_dir_btn.config(state='active')

    def ask_output_directory(self) -> None:
        """
        Creates a file dialog and enables and loads methods into Make List buttons.
        """
        # Ask user for directory
        self.output_dirname = tk.filedialog.askdirectory()

        if self.output_dirname:
            # Outputs message of selected directory to GUI
            self.selected_output_dir_label.config(text='Output Directory:\n{}'.format(self.output_dirname))

            # Make buttons active
            self.make_list_text_btn.config(
                state='active', command=partial(self.make_dir_tree_text, self.dirname, self.output_dirname)
            )
            self.make_list_excel_btn.config(
                state='active', command=partial(self.make_dir_tree_excel, self.dirname, self.output_dirname)
            )

    def make_dir_tree_text(self, directory: str, output_dir: str) -> None:
        """
        Creates a txt file of a Directory Tree, and outputs message to 'output' Label.

        :param directory: a valid directory
        :type directory: str
        :param output_dir: directory which outputted text file will be saved
        :type output_dir: str
        """
        core.list_directory_tree_text(directory, output_dir)

        if sys.platform.startswith('win32'):
            file_name = directory.split('\\')[-1]
            output_file_location = r'{output_dir}\{file}'.format(
                output_dir=output_dir,
                file='directory-tree-{}.txt'.format(file_name)
            )
        else:
            file_name = directory.split('/')[-1]
            output_file_location = '{output_dir}/{file}'.format(
                output_dir=output_dir,
                file='directory-tree-{}.txt'.format(file_name)
            )
        # Outputs message of file created to GUI
        self.output_label.config(text='Created text file:\n{}'.format(output_file_location))

    def make_dir_tree_excel(self, directory: str, output_dir: str) -> None:
        """
        Creates a xlsx file of a Directory Tree, and outputs message to 'output' Label.

        :param directory: directory to be recursive listed
        :type directory: str
        :param output_dir: directory which outputted text file will be saved
        :type output_dir: str
        """
        core.list_directory_tree_excel(directory, output_dir)

        if sys.platform.startswith('win32'):
            file_name = directory.split('\\')[-1]
            output_file_location = r'{output_dir}\{file}'.format(
                output_dir=output_dir,
                file='directory-tree-{}.xlsx'.format(file_name)
            )
        else:
            file_name = directory.split('/')[-1]
            output_file_location = '{output_dir}/{file}'.format(
                output_dir=output_dir,
                file='directory-tree-{}.xlsx'.format(file_name)
            )
        # Outputs message of file created to GUI
        self.output_label.config(text='Created excel file:\n{}'.format(output_file_location))


# Create the application
root = tk.Tk()
app = Application(master=root)

# Title and sizing
app.master.title('Directory Tree Lister')
app.master.minsize(400, 300)
app.master.maxsize(400, 300)
app.master.resizable(False, False)

# Start the program
app.mainloop()

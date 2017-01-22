import sys
from functools import partial
from tkinter import Tk, ttk, filedialog

from dtlister import core


class DirectoryTreeListerApp(ttk.Frame):
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
        self.grid(row=0, column=0, padx=15, pady=10, sticky='NSEW')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Choose a directory button
        self.ask_dir_btn = ttk.Button(self, text='Choose a directory to scan...', command=self.ask_directory, width=25)
        self.ask_dir_btn.grid(row=1, pady=2)

        # Choose a output directory button
        self.ask_output_dir_btn = ttk.Button(self, text='Choose an output directory...',
                                             command=self.ask_output_directory,
                                             state='disabled', width=25)
        self.ask_output_dir_btn.grid(row=2, pady=2)

        self.sep_1 = ttk.Separator(self)
        self.sep_1.grid(row=3, pady=5, sticky='EW')

        # Text button
        self.make_list_text_btn = ttk.Button(self, text="Create Text File Directory Tree", state='disabled', width=25)
        self.make_list_text_btn.grid(row=4, pady=2)

        # Excel button
        self.make_list_excel_btn = ttk.Button(self, text="Create Excel File Directory Tree", state='disabled', width=25)
        self.make_list_excel_btn.grid(row=5, pady=2)

        self.sep_2 = ttk.Separator(self)
        self.sep_2.grid(row=6, pady=5, sticky='EW')

        # Quit button
        self.quit_btn = ttk.Button(self, text="Quit", command=root.destroy, width=10)
        self.quit_btn.grid(row=7, pady=2)

        # Selected directory label
        self.selected_dir_label = ttk.Label(self, text='', justify='left', wraplength=250)
        self.selected_dir_label.grid(row=8, pady=5)

        # Selected output directory label
        self.selected_output_dir_label = ttk.Label(self, text='', justify='left', wraplength=250)
        self.selected_output_dir_label.grid(row=9, pady=5)

        # Output label
        self.output_label = ttk.Label(self, text='', justify='left', wraplength=250)
        self.output_label.grid(row=10, pady=5)

    def ask_directory(self) -> None:
        """
        Creates a file dialog and outputs select directory value to label.
        """
        # Ask user for directory
        self.dirname = filedialog.askdirectory()

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
        self.output_dirname = filedialog.askdirectory()

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
root = Tk()
root.configure(bg='#E7E7E7')
app = DirectoryTreeListerApp(master=root)

# Title and sizing
app.master.title('Directory Tree Lister 0.9')
app.master.minsize(290, 450)
app.master.maxsize(290, 550)
app.master.resizable(False, True)

# Start the program
app.mainloop()

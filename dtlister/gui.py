import sys
from tkinter import Tk, ttk, filedialog, Menu, messagebox

from dtlister import core


class DirectoryTreeListerApp(ttk.Frame):
    """
    Class consisting of Directory Tree Lister GUI methods.
    """

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.app_name = 'Directory Tree Lister'
        self.app_version = '0.9'

        # Set size, colour, and tile
        self.master.configure(bg='#E7E7E7')
        self.master.minsize(290, 450)
        self.master.maxsize(290, 550)
        self.master.resizable(False, True)
        self.master.title(self.app_name)
        self.pack()

        self.create_menubar()
        self.create_widgets()

    def create_menubar(self):
        """
        Create menubar.
        """
        self.menubar = Menu(self.master)

        # About menu dialog
        self.about_menu = Menu(self.menubar, name='apple', tearoff=False)
        self.menubar.add_cascade(menu=self.about_menu)
        self.about_menu.add_cascade(label='About {app}'.format(app=self.app_name), command=self.open_about_dialog)
        self.about_menu.add_separator()
        self.master.configure(menu=self.menubar)

        # File menu
        self.file_menu = Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Quit", command=self.master.destroy)

    def open_about_dialog(self):
        """
        Opens 'About' dialog.
        """
        messagebox.showinfo(message='{} {}\n\nCreates a recursive list of a directory and saves it as either a text or '
                                    'excel file.'.format(self.app_name, self.app_version))

    def create_widgets(self) -> None:
        """
        Creates Buttons and Labels.
        """
        # Grid setup
        self.grid(row=0, column=0, padx=15, pady=10, sticky='NSEW')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Choose directory buttons
        self.ask_dir_btn = ttk.Button(self, text='Choose a directory to scan...', command=self.ask_directory, width=25)
        self.ask_dir_btn.grid(row=1, pady=2)

        self.ask_output_dir_btn = ttk.Button(
            self, text='Choose an output directory...', command=self.ask_output_directory, state='disabled', width=25
        )
        self.ask_output_dir_btn.grid(row=2, pady=2)

        self.sep_1 = ttk.Separator(self)
        self.sep_1.grid(row=3, pady=5, sticky='EW')

        # Make list buttons
        self.make_list_text_btn = ttk.Button(
            self, text="Create Text File Directory Tree", width=25, command=self.make_dir_tree_text, state='disabled'
        )
        self.make_list_text_btn.grid(row=4, pady=2)

        self.make_list_excel_btn = ttk.Button(
            self, text="Create Excel File Directory Tree", width=25, command=self.make_dir_tree_excel, state='disabled'
        )
        self.make_list_excel_btn.grid(row=5, pady=2)

        self.sep_2 = ttk.Separator(self)
        self.sep_2.grid(row=6, pady=5, sticky='EW')

        # Quit button
        self.quit_btn = ttk.Button(self, text="Quit", command=self.master.destroy, width=10)
        self.quit_btn.grid(row=7, pady=2)

        # Labels
        self.selected_dir_label = ttk.Label(self, text='', justify='left', wraplength=250)
        self.selected_dir_label.grid(row=8, pady=5)

        self.selected_output_dir_label = ttk.Label(self, text='', justify='left', wraplength=250)
        self.selected_output_dir_label.grid(row=9, pady=5)

        self.output_label = ttk.Label(self, text='', justify='left', wraplength=250)
        self.output_label.grid(row=10, pady=5)

    def ask_directory(self) -> None:
        """
        Ask user for directory to be scanned, shows selected directory in GUI, and enables
        'Choose an output directory...' button.
        """
        self.chosen_scan_dir = filedialog.askdirectory()

        if self.chosen_scan_dir:
            self.selected_dir_label.config(text='Scan Directory:\n{}'.format(self.chosen_scan_dir))
            self.ask_output_dir_btn.config(state='active')

    def ask_output_directory(self) -> None:
        """
        Ask user for output directory, shows selected directory in GUI, and enables Create-List buttons.
        """
        self.chosen_output_dir = filedialog.askdirectory()

        if self.chosen_output_dir:
            self.selected_output_dir_label.config(text='Output Directory:\n{}'.format(self.chosen_output_dir))
            self.make_list_text_btn.config(state='active')
            self.make_list_excel_btn.config(state='active')

    def make_dir_tree_text(self) -> None:
        """
        Creates a txt file of a Directory Tree, and outputs message to GUI.
        """
        core.list_directory_tree_text(self.chosen_scan_dir, self.chosen_output_dir)

        if sys.platform.startswith('win32'):
            file_name = self.chosen_scan_dir.split('\\')[-1]
            output_file_location = r'{output_dir}\{file}'.format(
                output_dir=self.chosen_output_dir,
                file='directory-tree-{}.txt'.format(file_name)
            )
        else:
            file_name = self.chosen_scan_dir.split('/')[-1]
            output_file_location = '{output_dir}/{file}'.format(
                output_dir=self.chosen_output_dir,
                file='directory-tree-{}.txt'.format(file_name)
            )
        self.output_label.config(text='Created Text File:\n{}'.format(output_file_location))

    def make_dir_tree_excel(self) -> None:
        """
        Creates a xlsx file of a Directory Tree, and outputs message to GUI.
        """
        core.list_directory_tree_excel(self.chosen_scan_dir, self.chosen_output_dir)

        if sys.platform.startswith('win32'):
            file_name = self.chosen_scan_dir.split('\\')[-1]
            output_file_location = r'{output_dir}\{file}'.format(
                output_dir=self.chosen_output_dir,
                file='directory-tree-{}.xlsx'.format(file_name)
            )
        else:
            file_name = self.chosen_scan_dir.split('/')[-1]
            output_file_location = '{output_dir}/{file}'.format(
                output_dir=self.chosen_output_dir,
                file='directory-tree-{}.xlsx'.format(file_name)
            )
        self.output_label.config(text='Created Excel File:\n{}'.format(output_file_location))


def main():
    # Create and start the application
    root = Tk()
    app = DirectoryTreeListerApp(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()

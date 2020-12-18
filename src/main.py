""" Visualizing Climate Change against Education

main.py

This module executes the program and manages the GUI.

written by Kenneth Tran

"""

import prepare_data
import visualize_data
from data_classes import EducationData, ClimateData, EducationAttainment, WrongFileError

import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk

from typing import Dict, List, Tuple


# A mapping of string to EducationAttainment objects
EDUCATION_ATTAINMENTS = {e.value: e for e in EducationAttainment}


class App(tk.Tk):
    """This class represents the application and manages the different frames."""

    _education_data: Dict[str, List[EducationData]]
    _climate_data: Dict[str, List[ClimateData]]

    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)

        self.minsize(width=675, height=600)

        # Font for headers
        self.header_font = font.Font(family='Calibri', size=18, weight='bold')
        # Font for subheaders
        self.subheader_font = font.Font(family='Calibri', size=14)

        self.title('Climate Change and Education Visualizer')

        # Use container to stack frames
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create an instance of LoadDataPage
        load_data_page = LoadDataPage(parent=container, controller=self)
        load_data_page.grid(row=0, column=0, sticky='nsew')

        # Create an instance of MainPage
        main_page = MainPage(parent=container, controller=self)
        main_page.grid(row=0, column=0, sticky='nsew')

        # Store instances of pages in a dict
        self.pages = {'LoadDataPage': load_data_page, 'MainPage': main_page}

        # Display the load data page
        self.display_page('LoadDataPage')

    def display_page(self, page_name: str) -> None:
        """Display the given page by bringing it to the front."""
        self.pages[page_name].tkraise()

    def load_education_data(self, education_data: Dict[str, List[EducationData]]) -> None:
        """Load education data into the app."""
        self._education_data = education_data

        # Load countries into the main page country combobox
        self.pages['MainPage'].load_countries(tuple(sorted(education_data.keys())))

    def load_climate_data(self, climate_data: Dict[str, List[ClimateData]]) -> None:
        """Load education data into the app."""
        self._climate_data = climate_data

    def get_education_data(self) -> Dict[str, List[EducationData]]:
        """Return the loaded education data which is a dict with key of country name and
         value of list of EducationData"""
        return self._education_data

    def get_climate_data(self) -> Dict[str, List[ClimateData]]:
        """Return the loaded climate data which is a dict with key of country name and
         value of list of ClimateData"""
        return self._climate_data


class LoadDataPage(tk.Frame):
    """This class represents the load data page of the application, as a tk Frame."""

    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lbl_title = tk.Label(master=self, text='Climate Change and Education Visualizer', font=controller.header_font)
        lbl_title.pack(ipady=30)

        self.init_datasets_frame()

    def init_datasets_frame(self) -> None:
        """Initialize the choose datasets frame."""
        frm_datasets = tk.Frame(master=self, relief=tk.GROOVE, borderwidth=1)
        frm_datasets.pack(padx=10, pady=10)

        lbl_title = tk.Label(master=frm_datasets, text='Choose Datasets',
                             font=self.controller.subheader_font, pady=20)
        lbl_title.pack()

        def choose_education_data_file() -> None:
            """Open the file explorer to choose the education data file."""
            file_name = filedialog.askopenfilename(initialdir="/",
                                                   title="Choose a File",
                                                   filetypes=(("CSV Files", "*.csv"),))

            # Update components
            edit_entry(ent_education_data, file_name)

        def choose_climate_data_file() -> None:
            """Open the file explorer to choose the climate data file."""
            file_name = filedialog.askopenfilename(initialdir="/",
                                                   title="Choose a File",
                                                   filetypes=(("CSV Files", "*.csv"),))

            # Update components
            edit_entry(ent_climate_data, file_name)

        # Create a frame to hold the entries
        frm_form = tk.Frame(master=frm_datasets)
        frm_form.pack(padx=10, pady=10)

        # Education data widgets
        lbl_education_data = tk.Label(master=frm_form, text="Education Data")
        ent_education_data = tk.Entry(master=frm_form, width=75, state='readonly', readonlybackground="white")

        lbl_education_data.grid(row=0, column=0, sticky='e')
        ent_education_data.grid(row=0, column=1)

        btn_choose_education_data_file = tk.Button(master=frm_form, text="Choose File",
                                                   command=choose_education_data_file)
        btn_choose_education_data_file.grid(row=0, column=2)

        # Climate data widgets
        lbl_climate_data = tk.Label(master=frm_form, text="Climate Data", pady=5)
        ent_climate_data = tk.Entry(master=frm_form, width=75, state='readonly', readonlybackground="white")

        lbl_climate_data.grid(row=1, column=0, sticky='e')
        ent_climate_data.grid(row=1, column=1)

        btn_choose_climate_data_file = tk.Button(master=frm_form, text="Choose File", command=choose_climate_data_file)
        btn_choose_climate_data_file.grid(row=1, column=2)

        def load_data() -> None:
            """Load data command."""
            climate_file = ent_climate_data.get()
            education_file = ent_education_data.get()

            if climate_file == '' or education_file == '':
                tk.messagebox.showerror('Error', 'You must select both files.')

            lbl_output.config(text='Loading data...')

            def read_data() -> None:
                """Read the data."""

                try:
                    raw_education_data = prepare_data.read_raw_education_data(education_file)
                    raw_climate_data = prepare_data.read_raw_climate_data(climate_file)
                except WrongFileError as error:
                    tk.messagebox.showerror('Error', error)
                    lbl_output.config(text='')
                    return

                # Process the raw data
                processed_data = prepare_data.process_data(raw_education_data, raw_climate_data)

                # Pass the data to the controller App class
                self.controller.load_education_data(processed_data[0])
                self.controller.load_climate_data(processed_data[1])

                lbl_output.config(text='Loaded data!')

                self.after(100, lambda: self.controller.display_page('MainPage'))

            # Delay so that the label gets updated
            self.after(5, read_data)

        btn_load_data = tk.Button(master=frm_datasets, text='Load Data', command=load_data)
        btn_load_data.pack(padx=10, ipadx=10)

        lbl_output = tk.Label(master=frm_datasets)
        lbl_output.pack(pady=10)


class MainPage(tk.Frame):
    """This class represents the main page of the application where the user can interact with the data."""

    _cmb_country: ttk.Combobox
    _cmb_education_attainment: ttk.Combobox
    _cmb_start_age: ttk.Combobox
    _cmb_end_age: ttk.Combobox

    def __init__(self, parent, controller) -> None:
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lbl_title = tk.Label(master=self, text='Climate Change and Education Visualizer', font=controller.header_font)
        lbl_title.pack(ipady=10, pady=10)

        self.init_dataset_visualizer_frame()

    def init_dataset_visualizer_frame(self) -> None:
        """Initialize the configuration frame."""
        frm_dataset_visualizer = tk.Frame(master=self, relief=tk.GROOVE, borderwidth=1)
        frm_dataset_visualizer.pack(padx=10, pady=10)

        lbl_title = tk.Label(master=frm_dataset_visualizer, text='Dataset Visualizer',
                             font=self.controller.subheader_font, pady=20)
        lbl_title.pack()

        # Create a frame to hold the form
        frm_data_form = tk.Frame(master=frm_dataset_visualizer)
        frm_data_form.pack(padx=10, pady=10)

        # Country widgets
        lbl_country = tk.Label(master=frm_data_form, text="Country Name")
        self._cmb_country = ttk.Combobox(master=frm_data_form, width=75, state='readonly')

        lbl_country.grid(row=1, column=0, sticky='e')
        self._cmb_country.grid(row=1, column=1, pady=5)

        # Education Attainment widgets
        lbl_education_attainment = tk.Label(master=frm_data_form, text="Education Attainment")
        self._cmb_education_attainment = ttk.Combobox(master=frm_data_form, width=75, state='readonly')

        # Load EducationAttainment enum into the combobox
        self._cmb_education_attainment['values'] = tuple(e.value for e in EducationAttainment)
        self._cmb_education_attainment.current(0)

        lbl_education_attainment.grid(row=2, column=0, sticky='e')
        self._cmb_education_attainment.grid(row=2, column=1, pady=5)

        # Start and end age
        lbl_start_age = tk.Label(master=frm_data_form, text='Start Age')
        self._cmb_start_age = ttk.Combobox(master=frm_data_form, width=15, state='readonly')
        self._cmb_start_age['values'] = tuple(range(15, 75, 5))
        self._cmb_start_age.current(0)

        lbl_start_age.grid(row=3, column=0, padx=5, sticky='e')
        self._cmb_start_age.grid(row=3, column=1, pady=5, sticky='w')

        lbl_end_age = tk.Label(master=frm_data_form, text='End Age')
        self._cmb_end_age = ttk.Combobox(master=frm_data_form, width=15, state='readonly')
        self._cmb_end_age['values'] = tuple(range(19, 76, 5))
        self._cmb_end_age.current(0)

        lbl_end_age.grid(row=4, column=0, padx=5, sticky='e')
        self._cmb_end_age.grid(row=4, column=1, pady=5, sticky='w')

        def plot_datasets_command() -> None:
            """Plot the raw datasets."""
            country = self._cmb_country.get()
            education_attainment = self._cmb_education_attainment.get()
            start_age = int(self._cmb_start_age.get())
            end_age = int(self._cmb_end_age.get())

            if start_age >= end_age:
                tk.messagebox.showerror('Error', 'End age must be greater than start age.')
                return

            lbl_output.config(text='Plotting raw data...')

            # Delay so that the label gets updated
            self.after(5, lambda: (
                visualize_data.plot_datasets(country, start_age, end_age, self.controller.get_climate_data(),
                                             self.controller.get_education_data(),
                                             EDUCATION_ATTAINMENTS[education_attainment]),
                lbl_output.config(text='')
            ))

        def perform_regression_command() -> None:
            """Perform linear regression."""
            country = self._cmb_country.get()
            education_attainment = self._cmb_education_attainment.get()
            start_age = int(self._cmb_start_age.get())
            end_age = int(self._cmb_end_age.get())

            if start_age >= end_age:
                tk.messagebox.showerror('Error', 'End age must be less than start age.')
                return

            lbl_output.config(text='Performing linear regression...')

            # Delay so that the label gets updated
            self.after(5, lambda: (
                visualize_data.plot_datasets_and_linear_regression(country, start_age, end_age,
                                                                   EDUCATION_ATTAINMENTS[education_attainment],
                                                                   self.controller.get_climate_data(),
                                                                   self.controller.get_education_data()),
                lbl_output.config(text='')
            ))

        # Frame for the buttons
        frm_btns = tk.Frame(master=frm_dataset_visualizer)
        frm_btns.pack()

        btn_plot_raw_data = tk.Button(master=frm_btns, text='Plot Raw Data', command=plot_datasets_command)
        btn_plot_raw_data.grid(row=0, column=0, padx=5)

        btn_perform_regression = tk.Button(master=frm_btns, text='Perform Linear Regression',
                                           command=perform_regression_command)
        btn_perform_regression.grid(row=0, column=1, padx=5)

        lbl_output = tk.Label(master=frm_dataset_visualizer)
        lbl_output.pack(pady=10)

    def load_countries(self, countries: Tuple[str]) -> None:
        """Load a tuple of countries into the country combobox."""
        self._cmb_country['values'] = countries
        self._cmb_country.current(0)


def edit_entry(entry: tk.Entry, text: str):
    """Modify the text inside a tk Entry object."""

    # Get the state of the entry
    prev_state = str(entry['state'])

    # Make the entry editable
    entry.config(state='normal')
    entry.delete(0, 'end')
    entry.insert(0, text)

    # Return entry to normal state
    entry.config(state=prev_state)


def is_positive_float(value) -> bool:
    """Return whether the given argument is a positive float."""
    try:
        num = float(value)
        return num > 0
    except ValueError:
        return False


if __name__ == "__main__":
    # Start the app
    app = App()
    app.mainloop()

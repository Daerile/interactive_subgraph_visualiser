import pandas as pd
import tkinter as tk
import chardet
from tkinter import filedialog
from io import StringIO


class Loader:

    @classmethod
    def init_root(cls):
        """
        Initialize the root Tkinter object if it has not been initialized yet.
        This is used for the file dialog operations.
        """
        if not hasattr(cls, 'root'):
            cls.root = tk.Tk()
            cls.root.withdraw()

    @classmethod
    def save_file(cls, data_string):
        """
        Save a string of data to a file. The data string is assumed to be in CSV format.
        A file dialog is used to ask the user where to save the file.
        """
        cls.init_root()
        file_path = filedialog.asksaveasfilename(
            filetypes=(('CSV files', '*.csv'),),
            defaultextension=".csv"
        )
        if file_path:
            # Assuming data_string is a CSV formatted string
            df = pd.read_csv(StringIO(data_string), sep=';')
            df.to_csv(file_path, index=False, sep=';', encoding='utf-8')
            print(f"File has been saved to: {file_path}")
        else:
            print("No file selected. File not saved.")

    @classmethod
    def load_file(cls):
        """
        Load a file using a file dialog. The file types supported are CSV and Excel.
        The file is read using the appropriate pandas function based on its type.
        """
        cls.init_root()
        filetypes = (
            ('CSV files', '*.csv'),
            ('Excel files', '*.xlsx'),
        )

        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            print(f"File selected: {file_path}")
            return cls.read_file(file_path, file_path.split('.')[-1])
        else:
            print("No file selected.")
            return None

    @classmethod
    def read_file(cls, file_path, file_type):
        """
        Read a file given its path and type. The file types supported are CSV and Excel.
        For CSV files, the encoding is detected before reading the file.
        """
        if file_type == 'csv':
            with open(file_path, 'rb') as f:
                data = f.read()
            encoding_result = chardet.detect(data)
            encoding = encoding_result['encoding']
            try:
                read_data = pd.read_csv(file_path, sep=';', encoding=encoding)
                return read_data
            except pd.errors.EmptyDataError:
                print("File is empty.")
                return None
        elif file_type == 'xlsx':
            return pd.read_excel(file_path)
        else:
            print("Unsupported file type.")
            return None
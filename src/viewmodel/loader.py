import pandas as pd
import tkinter as tk
from tkinter import filedialog
from io import StringIO

class Loader:

    @classmethod
    def init_root(cls):
        if not hasattr(cls, 'root'):
            cls.root = tk.Tk()
            cls.root.withdraw()

    @classmethod
    def save_file(cls, data_string):
        cls.init_root()
        file_path = filedialog.asksaveasfilename(
            filetypes=(('CSV files', '*.csv'),),
            defaultextension=".csv"
        )
        if file_path:
            # Assuming data_string is a CSV formatted string
            df = pd.read_csv(StringIO(data_string), sep=';')
            df.to_csv(file_path, index=False, sep=';', encoding='cp1250')
            print(f"File has been saved to: {file_path}")
        else:
            print("No file selected. File not saved.")


    @classmethod
    def load_file(cls):
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
        if file_type == 'csv':
            return pd.read_csv(file_path, sep=';', encoding='cp1250')
        elif file_type == 'xlsx':
            return pd.read_excel(file_path)
        else:
            print("Unsupported file type.")
            return None



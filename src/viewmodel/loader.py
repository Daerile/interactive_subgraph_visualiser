import pandas as pd
import tkinter as tk
from tkinter import filedialog


class Loader:

    @classmethod
    def init_root(cls):
        if not hasattr(cls, 'root'):
            cls.root = tk.Tk()
            cls.root.withdraw()

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
            return pd.read_csv(file_path, sep=';')
        elif file_type == 'xlsx':
            return pd.read_excel(file_path)
        else:
            print("Unsupported file type.")
            return None



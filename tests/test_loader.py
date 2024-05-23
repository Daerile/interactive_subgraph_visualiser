import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from io import StringIO

from src.viewmodel.loader import Loader

class TestLoader(unittest.TestCase):

    @patch('src.viewmodel.loader.filedialog.askopenfilename')
    @patch('src.viewmodel.loader.tk.Tk')
    def test_load_file_csv(self, mock_tk, mock_askopenfilename):
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance

        mock_askopenfilename.return_value = 'test.csv'

        data = "col1;col2\nval1;val2"
        df = pd.read_csv(StringIO(data), sep=';')
        with patch('src.viewmodel.loader.Loader.read_file', return_value=df) as mock_read_file:
            result = Loader.load_file()
            mock_read_file.assert_called_once_with('test.csv', 'csv')
            self.assertTrue(result.equals(df))

    @patch('pandas.read_csv')
    @patch('src.viewmodel.loader.filedialog.asksaveasfilename')
    @patch('src.viewmodel.loader.tk.Tk')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_file(self, mock_open, mock_tk, mock_asksaveasfilename, mock_pandas_read_csv):
        mock_tk_instance = MagicMock()
        mock_tk.return_value = mock_tk_instance

        mock_asksaveasfilename.return_value = 'test_save.csv'

        data_string = "col1;col2\nval1;val2"

        Loader.save_file(data_string)

        mock_asksaveasfilename.assert_called_once()

        # Ensure read_csv is called with a StringIO object with the correct data
        args, kwargs = mock_pandas_read_csv.call_args
        self.assertEqual(args[0].getvalue(), data_string)
        self.assertEqual(kwargs['sep'], ';')

        # Ensure to_csv is called with the correct file path and parameters
        df = mock_pandas_read_csv.return_value
        df.to_csv.assert_called_once_with('test_save.csv', index=False, sep=';', encoding='utf-8')

    @patch('pandas.read_csv')
    @patch('src.viewmodel.loader.filedialog.askopenfilename')
    @patch('src.viewmodel.loader.tk.Tk')
    @patch('builtins.open', new_callable=mock_open, read_data='col1;col2\nval1;val2')
    @patch('src.viewmodel.loader.chardet.detect')
    def test_read_file_csv(self, mock_chardet_detect, mock_open, mock_tk, mock_askopenfilename, mock_pandas_read_csv):
        mock_chardet_detect.return_value = {'encoding': 'utf-8'}

        file_path = 'test.csv'

        df = Loader.read_file(file_path, 'csv')

        mock_pandas_read_csv.assert_called_once_with(file_path, sep=';', encoding='utf-8')


    @patch('src.viewmodel.loader.filedialog.askopenfilename')
    @patch('src.viewmodel.loader.tk.Tk')
    @patch('pandas.read_excel')
    def test_read_file_xlsx(self, mock_read_excel, mock_tk, mock_askopenfilename):
        df = pd.DataFrame({'col1': ['val1'], 'col2': ['val2']})
        mock_read_excel.return_value = df

        file_path = 'test.xlsx'

        result = Loader.read_file(file_path, 'xlsx')

        mock_read_excel.assert_called_once_with(file_path)
        self.assertTrue(result.equals(df))


if __name__ == '__main__':
    unittest.main()

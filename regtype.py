import pandas as pd
import re
from collections import defaultdict

class Busboy:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.regex_application_count = defaultdict(int)

    def remove_missing_values(self, strategy='drop', fill_value=None):
        if strategy == 'drop':
            self.df = self.df.dropna()
        elif strategy == 'fill':
            self.df = self.df.fillna(fill_value)
        else:
            raise ValueError("Strategy must be 'drop' or 'fill'")
        return self

    def remove_duplicates(self):
        self.df = self.df.drop_duplicates()
        return self

    def convert_data_types(self, column_types: dict):
        self.df = self.df.astype(column_types)
        return self

    def apply_regex_to_columns(self, regex_list: dict):
        """
        Apply a list of regex patterns to the DataFrame columns based on column data type.

        Parameters:
        regex_list (dict): A dictionary where keys are data types and values are lists of regex patterns.
        """
        for column in self.df.columns:
            column_type = str(self.df[column].dtype)
            if column_type in regex_list:
                patterns = regex_list[column_type]
                for i, value in enumerate(self.df[column]):
                    for pattern in patterns:
                        if pd.notnull(value) and re.search(pattern, str(value)):
                            self.df.at[i, column] = re.sub(pattern, '', str(value))
                            self.regex_application_count[column] += 1
                            break  # First regex match wins
        return self

    def get_cleaned_data(self):
        return self.df

    def get_regex_application_count(self):
        return dict(self.regex_application_count)

# Usage example:
if __name__ == "__main__":
    # Sample DataFrame
    data = {
        'A': [1, 2, None, 4, 4],
        'B': ['a', 'b', 'b', 'c', None],
        'C': ['1.1', '2.2 text', '3.3', 'remove4.4', '5.5'],
        'D': [pd.Timestamp('20230101'), pd.Timestamp('20230201'), None, pd.Timestamp('20230301'), pd.Timestamp('20230401')],
        'E': [True, False, True, False, None],
        'F': [pd.Timestamp('20230101'), pd.Timestamp('20230201'), None, pd.Timestamp('20230301'), pd.Timestamp('20230401')],
    }
    df = pd.DataFrame(data)

    # Create a Busboy object
    cleaner = Busboy(df)

    # Define regex patterns to apply
    regex_patterns = {
        'object': [r'\D'],  # Remove non-digit characters for object columns
        'float64': [r'[^\d.]'],  # Remove non-digit characters except dot for float columns
        'int64': [r'\D'],  # Remove non-digit characters for int columns
        'datetime64[ns]': [r'.*'],  # Replace all content in datetime columns
        'bool': [r'False']  # Remove 'False' for boolean columns
    }

    # Clean the DataFrame
    cleaned_df = (cleaner
                  .remove_missing_values(strategy='fill', fill_value=0)
                  .remove_duplicates()
                  .apply_regex_to_columns(regex_patterns)
                  .convert_data_types({'A': 'int64', 'C': 'float64'})
                  .get_cleaned_data())

    # Print the cleaned DataFrame
    print(cleaned_df)

    # Print regex application count
    print(cleaner.get_regex_application_count())

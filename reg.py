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
        Apply a list of regex patterns to the DataFrame columns.

        Parameters:
        regex_list (dict): A dictionary where keys are column names and values are lists of regex patterns.
        """
        for column, patterns in regex_list.items():
            if column in self.df.columns:
                for i, value in enumerate(self.df[column]):
                    for pattern in patterns:
                        if pd.notnull(value) and re.search(pattern, str(value)):
                            self.df.at[i, column] = re.sub(pattern, '', str(value))
                            self.regex_application_count[column] += 1
                            break  # First regex match wins
            else:
                raise ValueError(f"Column '{column}' not found in DataFrame")
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
        'C': ['1.1', '2.2 text', '3.3', 'remove4.4', '5.5']
    }
    df = pd.DataFrame(data)

    # Create a Busboy object
    cleaner = Busboy(df)

    # Define regex patterns to apply
    regex_patterns = {
        'C': [r'\D']  # Remove non-digit characters from column 'C'
    }

    # Clean the DataFrame
    cleaned_df = (cleaner
                  .remove_missing_values(strategy='fill', fill_value=0)
                  .remove_duplicates()
                  .convert_data_types({'A': 'int64', 'C': 'float64'})
                  .apply_regex_to_columns(regex_patterns)
                  .get_cleaned_data())

    # Print the cleaned DataFrame
    print(cleaned_df)

    # Print regex application count
    print(cleaner.get_regex_application_count())

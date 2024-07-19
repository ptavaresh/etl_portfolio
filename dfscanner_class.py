import pandas as pd
import re
from collections import defaultdict

class DFScanner:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.regex_application_count = defaultdict(int)
        self.change_report = pd.DataFrame(columns=['Row', 'Column', 'Regex Pattern'])

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
        for column, dtype in column_types.items():
            if dtype == 'int64':
                self.df[column] = pd.to_numeric(self.df[column], errors='coerce').fillna(0).astype(int)
            elif dtype == 'float64':
                self.df[column] = pd.to_numeric(self.df[column], errors='coerce').fillna(0.0).astype(float)
            else:
                self.df[column] = self.df[column].astype(dtype)
        return self

    def match_regex_patterns(self, value, patterns):
        """
        Check if a value matches any of the regex patterns and count the matches.

        Parameters:
        value (str): The value to check against regex patterns.
        patterns (list): A list of regex patterns.

        Returns:
        bool: True if any pattern matches, False otherwise.
        """
        for pattern in patterns:
            if re.search(pattern, value):
                return True, pattern
        return False, None

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
                for i, value in self.df[column].items():
                    if pd.notnull(value):
                        matched, pattern = self.match_regex_patterns(str(value), patterns)
                        if matched:
                            original_value = str(value)
                            new_value = re.sub(pattern, '', original_value)
                            self.df.at[i, column] = new_value
                            self.regex_application_count[column] += 1
                            self.log_change(i, column, pattern)
        return self

    def log_change(self, row, column, pattern):
        """
        Log changes made by the regex application.

        Parameters:
        row (int): The row index where the change occurred.
        column (str): The column name where the change occurred.
        pattern (str): The regex pattern applied.
        """
        change_record = pd.DataFrame({'Row': [row], 'Column': [column], 'Regex Pattern': [pattern]})
        self.change_report = pd.concat([self.change_report, change_record], ignore_index=True)

    def scan_values(self, patterns):
        """
        Scan each value in the DataFrame to check if it matches any pattern from a list of regex patterns.

        Parameters:
        patterns (list): A list of regex patterns to check against.

        Returns:
        bool: True if any value matches any pattern, False otherwise.
        """
        for column in self.df.columns:
            for value in self.df[column]:
                if pd.notnull(value):
                    matched, _ = self.match_regex_patterns(str(value), patterns)
                    if matched:
                        return True
        return False

    def get_cleaned_data(self):
        return self.df

    def get_regex_application_count(self):
        return dict(self.regex_application_count)

    def get_change_report(self):
        return self.change_report

import pandas as pd
import re
from collections import defaultdict
import time  # Importing the time module

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


    def scan_values(self, patterns: list) -> bool:
        """
        This function scans the dataframe to see if any value in the dataframe 
        matches any of the provided regex patterns. Returns True if at least 
        one match is found, otherwise returns False.

        :param patterns: List of regex patterns to search for in the dataframe.
        :return: Boolean indicating if any match was found.
        """
        
        # Start the timer
        start_time = time.time()

        # Pre-compile all regex patterns as non-capturing for efficiency
        # This converts (pattern) to (?:pattern) to make it non-capturing
        compiled_patterns = [re.compile(re.sub(r'\((?!\?:)', '(?:', pattern)) for pattern in patterns]

        # Iterate over columns with string-like data (e.g., object columns)
        for column in self.df.select_dtypes(include=['object']).columns:
            # Use vectorized string matching via str.contains for better performance
            for pattern in compiled_patterns:
                # Use str.contains() with any() to short-circuit when a match is found
                if self.df[column].astype(str).str.contains(pattern, regex=True, na=False).any():
                    # End the timer and calculate elapsed time
                    end_time = time.time()
                    execution_time = end_time - start_time
                    print(f"scan_values executed in: {execution_time:.4f} seconds")
                    return True

        # If no match is found in any column
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"scan_values executed in: {execution_time:.4f} seconds")

        return False


    def scan_and_compare_regex(self, regex_list):
        """
        Compares each value in the DataFrame against a list of regular expressions.
        
        :param df: DataFrame to scan.
        :param regex_list: List of regular expressions.
        :return: DataFrame of booleans where True indicates that at least one regex matched.
        """
        # Function to compare each value with the list of regex patterns
        def compare_with_regex(value):
            for regex in regex_list:
                if re.search(regex, str(value)):  # Convert to string in case of numeric values
                    return True
            return False
        
        # Apply the comparison function to each value in the DataFrame
        return self.df.applymap(compare_with_regex)

    def is_dataframe_clean(self, regex_list):
        """
        Checks if the DataFrame is clean or dirty based on regex matching.
        
        A DataFrame is considered 'dirty' if any value matches any regex in the list.
        It's considered 'clean' if none of the values match any of the regex patterns.

        :param df: DataFrame to scan.
        :param regex_list: List of regular expressions.
        :return: True if the DataFrame is clean (no matches), False if dirty (at least one match).
        """
        # Function to compare each value with the list of regex patterns
        def match_any_regex(value):
            for regex in regex_list:
                if re.search(regex, str(value)):  # Convert to string to handle different types
                    return True
            return False
        
        # Apply the regex matching function to the entire DataFrame and check if any value matches
        return not self.df.applymap(match_any_regex).any().any()

    def is_dataframe_clean2(self, regex_list):
        """
        Checks if the DataFrame is clean or dirty based on regex matching.

        A DataFrame is considered 'dirty' if any value matches any regex in the list.
        It's considered 'clean' if none of the values match any of the regex patterns.

        :param df: DataFrame to scan.
        :param regex_list: List of regular expressions.
        :return: True if the DataFrame is clean (no matches), False if dirty (at least one match).
        """
        # Convert capturing groups in regex to non-capturing groups (avoids warnings)
        non_capturing_regex_list = [re.sub(r'\((?!\?)', '(?:', regex) for regex in regex_list]
        
        # Combine all regex patterns into one string with OR operator
        combined_pattern = '|'.join(non_capturing_regex_list)
        
        # Apply the regex to the entire DataFrame and check for any match
        mask = self.df.astype(str).apply(lambda col: col.str.contains(combined_pattern, regex=True, na=False))
        
        # If any value matches, the DataFrame is dirty, otherwise it's clean
        return not mask.any().any()

    def get_cleaned_data(self):
        return self.df

    def get_regex_application_count(self):
        return dict(self.regex_application_count)

    def get_change_report(self):
        return self.change_report

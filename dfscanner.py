import pandas as pd
from dfscanner_class import DFScanner

# Sample DataFrame
data = {
    'A': [1, 2, None, 4, 4],
    'B': ['a', 'b', 'b', 'c', None],
    'C': ['1.1', '2.2 text', '3.3', 'remove4.4', '5.5'],
    'D': [pd.Timestamp('20230101'), pd.Timestamp('20230201'), None, pd.Timestamp('20230301'), pd.Timestamp('20230401')],
    'E': [True, False, True, False, None]
}
df = pd.DataFrame(data)

# Create a DFScanner object
scanner = DFScanner(df)

# Define regex patterns to apply
regex_patterns = {
    'object': [r'\D'],  # Remove non-digit characters for object columns
    'float64': [r'[^\d.]'],  # Remove non-digit characters except dot for float columns
    'int64': [r'\D'],  # Remove non-digit characters for int columns
    'datetime64[ns]': [r'.*'],  # Replace all content in datetime columns
    'bool': [r'False']  # Remove 'False' for boolean columns
}

# Clean the DataFrame
cleaned_df = (scanner
              .remove_missing_values(strategy='fill', fill_value=0)
              .remove_duplicates()
              .apply_regex_to_columns(regex_patterns)
              .convert_data_types({'A': 'int64', 'C': 'float64'})
              .get_cleaned_data())

# Print the cleaned DataFrame
print(cleaned_df)

# Print regex application count
print(scanner.get_regex_application_count())

# Print change report
print(scanner.get_change_report())

import pandas as pd
import yaml
from dfscanner_class import DFScanner

def load_config(config_path='config.yml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Load configuration
config = load_config()

# Sample DataFrame
data = {
    'A': [1, 2, None, 4, '4'],
    'B': ['a', 'b', 'b', 'c', None],
    'C': ['1.1', '2.2 text', '3.3', 'remove4.4', '5.5'],
    'D': [pd.Timestamp('20230101'), pd.Timestamp('20230201'), None, pd.Timestamp('20230301'), pd.Timestamp('20230401')],
    'E': [True, False, True, False, None]
}
df = pd.DataFrame(data)

# Create a DFScanner object
scanner = DFScanner(df)

# Retrieve regex patterns from config
regex_patterns = config['regex_patterns']

# Clean the DataFrame
cleaned_df = (scanner
              .remove_missing_values(strategy='fill', fill_value=0)
              .remove_duplicates()
              .apply_regex_to_columns(regex_patterns)
              .convert_data_types({'A': 'int64', 'C': 'float64'})
              .get_cleaned_data())

# Print the cleaned DataFrame
#print(cleaned_df)

# Print regex application count
#print(scanner.get_regex_application_count())

# Print change report
#print(scanner.get_change_report())

# Scan the DataFrame for matches with a new set of regex patterns
new_regex_patterns = [r'\d', r'[a-z]']  # Example patterns
matches_found = scanner.scan_values(new_regex_patterns)

# Print whether any matches were found
print("Matches found:", matches_found)

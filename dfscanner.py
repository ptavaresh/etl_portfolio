import pandas as pd
import yaml
import argparse
from dfscanner_class import DFScanner

def load_config(config_path='config.yml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process a DataFrame using DFScanner.')
    parser.add_argument('-scan', action='store_true', help='Run scan_values function to check for regex matches')
    parser.add_argument('-apply_regex', action='store_true', help='Apply regex patterns to DataFrame columns')
    parser.add_argument('-remove_missing', action='store_true', help='Remove missing values from DataFrame')
    parser.add_argument('-remove_duplicates', action='store_true', help='Remove duplicate rows from DataFrame')
    parser.add_argument('-convert_types', action='store_true', help='Convert column data types')
    args = parser.parse_args()

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

    # Execute based on arguments
    if args.scan:
        new_regex_patterns = config['scan_patterns']  # Load scan patterns from config
        matches_found = scanner.scan_values(new_regex_patterns)
        print("Matches found:", matches_found)

    if args.apply_regex:
        regex_patterns = config['regex_patterns']
        scanner.apply_regex_to_columns(regex_patterns)
        print(scanner.get_cleaned_data())
        print(scanner.get_regex_application_count())
        print(scanner.get_change_report())

    if args.remove_missing:
        scanner.remove_missing_values(strategy='fill', fill_value=0)
        print("After removing missing values:")
        print(scanner.get_cleaned_data())

    if args.remove_duplicates:
        scanner.remove_duplicates()
        print("After removing duplicates:")
        print(scanner.get_cleaned_data())

    if args.convert_types:
        column_types = {'A': 'int64', 'C': 'float64'}
        scanner.convert_data_types(column_types)
        print("After converting data types:")
        print(scanner.get_cleaned_data())

if __name__ == '__main__':
    main()

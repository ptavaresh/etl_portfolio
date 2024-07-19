import pandas as pd
import numpy as np


import re

def clean_string(value):
    if pd.isna(value):
        return value
    value = str(value)
    value = value.strip()
    value = re.sub(r'\s+', ' ', value)
    return value


class DataCleaner:
    def __init__(self, df):
        self.df = df

    def clean_column(self, column_name):
        dtype = self.df[column_name].dtype
        if dtype == 'object':
            self.df[column_name] = self.df[column_name].apply(clean_string)
        elif np.issubdtype(dtype, np.number):
            self.df[column_name] = self.df[column_name].apply(self.clean_number)
        elif np.issubdtype(dtype, np.datetime64):
            self.df[column_name] = self.df[column_name].apply(self.clean_date)
        else:
            print(f"No cleaning function for dtype: {dtype}")

    def clean_number(self, value):
        if pd.isna(value):
            return value
        try:
            return float(value)
        except ValueError:
            return np.nan

    def clean_date(self, value):
        if pd.isna(value):
            return value
        try:
            return pd.to_datetime(value, errors='coerce')
        except Exception:
            return np.nan

    def clean_dataframe(self):
        for column in self.df.columns:
            self.clean_column(column)
        return self.df

import re

def clean_string(value):
    if pd.isna(value):
        return value
    value = str(value)
    value = value.strip()
    value = re.sub(r'\s+', ' ', value)
    return value

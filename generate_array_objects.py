import pandas as pd
import json

def generate_array_objects(csv_file_path):
    df = pd.read_csv(csv_file_path)

    df.columns = [col.lower() for col in df.columns]

    json_records = df.to_dict(orient="records")

    wrapped_data = json_records

    return wrapped_data

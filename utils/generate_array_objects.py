import pandas as pd

def generate_array_objects(csv_file_path):
    df = pd.read_csv(csv_file_path)

    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    json_records = df.to_dict(orient="records")

    wrapped_data = json_records

    return wrapped_data

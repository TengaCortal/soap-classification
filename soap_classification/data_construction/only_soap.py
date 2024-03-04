import pandas as pd
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "resources/processed_data")
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps/by_clinic")

if __name__ == "__main__":
    # Iterate over each folder in DATA_PATH
    for folder_name in os.listdir(DATA_PATH):
        folder_path = os.path.join(DATA_PATH, folder_name)
        if os.path.isdir(folder_path):
            # Read the CSV file within each folder
            csv_file_path = os.path.join(folder_path, "DB_soap_orderCode.csv")
            df = pd.read_csv(csv_file_path)

            # Create a new DataFrame with just the first column
            new_df = pd.DataFrame(df.iloc[:, 0])

            # Generate the new filename based on the last 5 characters of the folder name
            new_csv_filename = folder_name[-5:] + "_soap.csv"

            # Save the new DataFrame to the specified CSV file
            new_df.to_csv(os.path.join(SOAPS_PATH, new_csv_filename), index=False)

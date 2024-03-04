import pandas as pd
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "resources/processed_data")
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps/by_clinic")

if __name__ == "__main__":
    # Read the initial CSV file
    df = pd.read_csv(
        os.path.join(DATA_PATH, "processed_data_10213/DB_soap_orderCode.csv")
    )

    # Create a new DataFrame with just the first column
    new_df = pd.DataFrame(df.iloc[:, 0])

    # Specify the filename or path for the new CSV file
    new_csv_filename = "10213_soap.csv"

    # Save the new DataFrame to the specified CSV file
    new_df.to_csv(os.path.join(SOAPS_PATH, new_csv_filename), index=False)

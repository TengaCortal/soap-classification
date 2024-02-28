import pandas as pd
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps")

if __name__ == "__main__":
    # Initialize an empty DataFrame to store the combined data
    combined_df = pd.DataFrame(columns=["Soap"])

    # Loop through each file in the directory
    for filename in os.listdir(os.path.join(SOAPS_PATH, "by_clinic")):
        if filename.endswith(".csv"):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(os.path.join(SOAPS_PATH, filename))
            # Append the DataFrame to the combined DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Write the combined DataFrame to a single CSV file
    combined_df.to_csv(os.path.join(SOAPS_PATH, "combined_soaps.csv"), index=False)

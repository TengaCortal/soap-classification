import pandas as pd
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_PATH, "resources/processed_data")
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps/by_clinic")

if __name__ == "__main__":
    all_dfs = []
    # Iterate over each folder in DATA_PATH
    for folder_name in os.listdir(DATA_PATH):
        folder_path = os.path.join(DATA_PATH, folder_name)
        if os.path.isdir(folder_path):
            # Read the CSV file within each folder
            csv_file_path = os.path.join(folder_path, "DB_soap_orderCode.csv")
            orderDB_csv = os.path.join(folder_path, "orderDB.csv")
            df = pd.read_csv(csv_file_path)
            df_orderDB = pd.read_csv(orderDB_csv)
            df_orderDB["order_code"] = df_orderDB["order_code"].astype(int)
            # Create a dictionary from the second DataFrame
            order_dict = pd.Series(
                df_orderDB.order_name.values, index=df_orderDB.order_code
            ).to_dict()

            print(order_dict)
            # Create a new DataFrame with just the first column
            new_df = pd.DataFrame(df.iloc[:, [0, 1, 2]])
            new_df["order_codes"] = new_df["order_codes"].apply(
                lambda x: (
                    [int(code) for code in eval(x)]
                    if isinstance(x, str)
                    else [int(code) for code in x]
                )
            )
            new_df["order_codes"] = new_df["order_codes"].apply(
                lambda codes: [order_dict.get(code) for code in codes]
            )
            # Generate the new filename based on the last 5 characters of the folder name
            new_csv_filename = folder_name[-5:] + "_soap_disease_order.csv"

            # Save the new DataFrame to the specified CSV file
            new_df.to_csv(os.path.join(SOAPS_PATH, new_csv_filename), index=False)

            # Append the new_df to the list
            all_dfs.append(new_df)

    # Concatenate all DataFrames in the list
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Save the combined DataFrame to a new CSV file
    combined_csv_path = os.path.join(
        os.path.join(BASE_PATH, "resources/soaps"), "soap_disease_order.csv"
    )
    combined_df.to_csv(combined_csv_path, index=False)

import pandas as pd
import os
from sklearn.utils import shuffle

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps")

sub_sections_df = pd.read_csv(os.path.join(SOAPS_PATH, "sub_sections.csv"))
obj_sections_df = pd.read_csv(os.path.join(SOAPS_PATH, "obj_sections.csv"))
asm_sections_df = pd.read_csv(os.path.join(SOAPS_PATH, "asm_sections.csv"))
pls_sections_df = pd.read_csv(os.path.join(SOAPS_PATH, "pln_sections.csv"))

# Add a new column "SOAP" and set its value
sub_sections_df["label"] = "S"
obj_sections_df["label"] = "O"
asm_sections_df["label"] = "A"
pls_sections_df["label"] = "P"

# Open a new CSV file to write
with open(os.path.join(SOAPS_PATH, "labeled_dataset.csv"), "w") as output_file:
    output_file.write("SOAP,label\n")  # Write header

    # Iterate through each dataframe and write rows to the new CSV file
    for df in [sub_sections_df, obj_sections_df, asm_sections_df, pls_sections_df]:
        for index, row in df.iterrows():
            output_file.write(
                f"{row['SUB']},{row['label']}\n"
                if "SUB" in row
                else (
                    f"{row['OBJ']},{row['label']}\n"
                    if "OBJ" in row
                    else (
                        f"{row['ASM']},{row['label']}\n"
                        if "ASM" in row
                        else f"{row['PLN']},{row['label']}\n"
                    )
                )
            )

labeled_dataset_df = pd.read_csv(os.path.join(SOAPS_PATH, "labeled_dataset.csv"))
shuffled_labeled_dataset_df = shuffle(labeled_dataset_df)

# Write the shuffled dataset back to the CSV file
shuffled_labeled_dataset_df.to_csv(
    os.path.join(SOAPS_PATH, "labeled_dataset.csv"), index=False
)

import pandas as pd
import os
import ast
import re
import csv
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
DATA_PATH = os.path.join(BASE_PATH, "resources/processed_data")
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps/by_clinic")


# Function to extract name from the dictionary string
def extract_name(d):
    d_dict = ast.literal_eval(d)  # Convert string to dictionary
    return d_dict["name"]


# Function to map age ranges to labels
def map_age_to_label(age):
    if age >= 0 and age <= 17:
        return "youth"
    elif age >= 18 and age <= 64:
        return "adult"
    else:
        return "elder"


# Function to replace patterns with "SUB:"
def replace_sub(text):
    """Replaces certain substrings in the input text with predefined abbreviations.


    Args:
        text (str): The input text to be processed.

    Returns:
        str: The modified text with substitutions applied.
    """
    text = re.sub(S_pattern, " SUB:", text)
    text = re.sub(O_pattern, " OBJ:", text)
    text = re.sub(A_pattern, " ASM:", text)
    text = re.sub(P_pattern, " PLN:", text)
    return text


# Function to remove unnecessary characters and patternss
def clean_text(text):
    """Cleans the input text by removing unnecessary characters and specified patterns.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text after removing unnecessary characters and specified patterns.
    """
    # Remove unnecessary characters
    cleaned_text = re.sub(pattern_to_remove, "", text)
    # Remove specified patterns following SUB:, OBJ:, ASM:, or PLN:
    cleaned_text = re.sub(pattern_to_replace, r"\1", cleaned_text)
    cleaned_text = re.sub(pattern_to_replace, r"\1", cleaned_text)
    cleaned_text = re.sub(pattern_X, "SUB:", cleaned_text)
    return cleaned_text


# Function to remove rows containing a certain pattern
def remove_rows_with_pattern(dataframe, key, pattern):
    """Removes rows from the DataFrame that contain a specified pattern.

    Args:
        dataframe (DataFrame): The pandas DataFrame from which rows will be removed.
        pattern (str): The pattern to search for within DataFrame rows.

    Returns:
        DataFrame: The modified DataFrame with rows containing the specified pattern removed.
    """
    return dataframe[~dataframe[key].str.contains(pattern)]


def extract_section(fairness_df, section):
    """
    Extracts the specified section from each SOAP note in the DataFrame.

    Args:
    - soaps_df (DataFrame): DataFrame containing SOAP notes.
    - section (str): Section to extract (SUB, OBJ, ASM, or PLN).

    Returns:
    - DataFrame: DataFrame containing only the specified section.
    """
    new_rows = []
    for index, row in fairness_df.iterrows():
        start_index = str(row.iloc[-1]).find(section) + len(section) + 1
        if section == "X":
            end_index = str(row.iloc[-1]).find("SUB")
        elif section == "SUB":
            end_index = str(row.iloc[-1]).find("OBJ")
        elif section == "OBJ":
            end_index = str(row.iloc[-1]).find("ASM")
        elif section == "ASM":
            end_index = str(row.iloc[-1]).find("PLN")
        else:
            end_index = len(str(row.iloc[-1]))
        section_text = str(row.iloc[-1])[start_index:end_index]

        new_row = list(row[:-1])
        new_row.append(section_text)
        new_row.append(section)
        new_rows.append(new_row)  # Append the new row to the list

    # Create a new DataFrame from the list of new rows
    new_df = pd.DataFrame(new_rows)

    return new_df


def create_section_csv(cleaned_classified_fairness_path, output_dir):
    """
    Creates separate CSV files for each section (SUB, OBJ, ASM, and PLN) from the cleaned and classified SOAP notes.

    Args:
    - cleaned_classified_soaps_path (str): Path to the cleaned and classified SOAP notes CSV file.
    - output_dir (str): Directory to save the section CSV files.
    """
    # Read the cleaned and classified SOAP notes CSV file
    soaps_df = pd.read_csv(cleaned_classified_fairness_path)
    # Extract and save each section as a separate CSV file
    sections = ["X", "SUB", "OBJ", "ASM", "PLN"]
    for section in sections:
        section_df = extract_section(soaps_df, section)
        output_path = os.path.join(output_dir, f"{section.lower()}_sections.csv")
        section_df.to_csv(output_path, index=False)
        print(f"{section} section CSV file saved to: {output_path}")


if __name__ == "__main__":
    # Iterate over each folder in DATA_PATH
    for folder_name in os.listdir(DATA_PATH):
        folder_path = os.path.join(DATA_PATH, folder_name)
        if os.path.isdir(folder_path):
            # Read the CSV file within each folder
            csv_file_path = os.path.join(folder_path, "raw_data.csv")
            df = pd.read_csv(csv_file_path)

            # Sort the DataFrame by 'patient number' column
            df.sort_values(by="patient_no", inplace=True)

            # Drop duplicates keeping the first occurrence (which is the earliest based on sorting)
            df.drop_duplicates(subset="patient_no", keep="first", inplace=True)

            # Reset index to make it sequential
            df.reset_index(drop=True, inplace=True)

            columns_to_drop = [
                "chart_id",
                "patient_basic",
                "interview",
                "birth_date",
                "insurances",
                "recipe_category",
                "recipe_medical_class",
                "recipe_quantity",
                "recipe_unit",
                "direction_usage",
                "recipe_items",
                "order_name",
                "order_code",
                "accept_datetime",
            ]
            df.drop(columns=columns_to_drop, inplace=True)

            # Remove double quotes from the "soap" column
            df["soap"] = df["soap"].str.replace('"', "")

            # Apply the function to the "department" column
            df["department"] = df["department"].apply(extract_name)

            df["physician"] = df["physician"].apply(extract_name)

            # Apply the function to the "age" column
            df["age"] = df["age"].apply(map_age_to_label)

            # Generate the new filename based on the last 5 characters of the folder name
            new_csv_filename = folder_name[-5:] + "_fairness.csv"

            # Save the new DataFrame to the specified CSV file
            df.to_csv(os.path.join(SOAPS_PATH, new_csv_filename), index=False)

    # Initialize an empty DataFrame to store the combined data
    combined_df = pd.DataFrame()

    # Loop through each file in the directory
    for filename in os.listdir(os.path.join(SOAPS_PATH)):
        if filename.endswith("fairness.csv"):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(os.path.join(os.path.join(SOAPS_PATH), filename))
            # Append the DataFrame to the combined DataFrame
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Write the combined DataFrame to a single CSV file
    combined_df.drop(columns="yakkakjncd", inplace=True)
    combined_df.to_csv(
        os.path.join(BASE_PATH, "fairness/combined_fairness.csv"), index=False
    )

    # Define the regex pattern
    pattern = re.compile(
        r'(?=(。S\)| S。|。S）|。S  |"S|S:|\(S\)|（S）|nS|S：|"S。|。S。|S\.|。Ｓ|Ｓ）|<S>|S\))).*(?=(。O\)| O。|。O）|。O |O:|\(O\)|（O）|nO|O：|。O。|O\.|。Ｏ|Ｏ）|<O>|O\))).*(?=(。A\)| A。|。A）|。A |A:|\(A\)|（A）|nA|A：|。A。|A\.|。Ａ|Ａ）|<A>|A\))).*(?=(。P\)| P。|。P）|。P |P:|\(P\)|（P）|nP|P：|。P。|P\.|。Ｐ|Ｐ）|<P>|P\)))'
    )

    with open(
        os.path.join(BASE_PATH, "fairness/combined_fairness.csv"), "r"
    ) as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)

        # Initialize a list to store rows matching the pattern
        matched_rows = []

        # Iterate through each row in the CSV file
        for row in reader:
            # Join the row elements into a single string
            row_str = ",".join(row)

            # Check if the regex pattern is in the row
            if pattern.search(row_str):
                # If the pattern is found, append the row to the list
                matched_rows.append(row)

    matched_rows.insert(
        0,
        [
            "clinic_id",
            "patient_no",
            "department",
            "physician",
            "diseases",
            "gender_type",
            "age",
            "soap",
        ],
    )

    # Write the matched rows to a new CSV file
    with open(
        os.path.join(BASE_PATH, "fairness/classified_fairness.csv"), "w", newline=""
    ) as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the matched rows to the new CSV file
        for row in matched_rows:
            writer.writerow(row)

    unified_df = df = pd.read_csv(
        os.path.join(BASE_PATH, "fairness/classified_fairness.csv")
    )

    df["soap"] = "X:" + df["soap"].astype(str)

    # Define the pattern
    S_pattern = re.compile(
        r'。S\)| S。|。S）|。S |"S|S:|\(S\)|（S）|nS|S：|"S。|。S。|S\.|。Ｓ|Ｓ）|<S>|S\)'
    )
    O_pattern = re.compile(
        r"。O\)| O。|。O）|。O |O:|\(O\)|（O）|nO|O：|。O。|O\.|。Ｏ|Ｏ）|<O>|O\)"
    )
    A_pattern = re.compile(
        r"。A\)| A。|。A）|。A |A:|\(A\)|（A）|nA|A：|。A。|A\.|。Ａ|Ａ）|<A>|A\)"
    )
    P_pattern = re.compile(
        r"。P\)| P。|。P）|。P |P:|\(P\)|（P）|nP|P：|。P。|P\.|。Ｐ|Ｐ）|<P>|P\)"
    )

    unified_df["soap"] = df["soap"].apply(replace_sub)
    # Save the modified DataFrame to a new CSV file
    unified_df.to_csv(
        os.path.join(BASE_PATH, "fairness/unified_syntax_fairness.csv"),
        index=False,
        header=False,
    )

    cleaned_soaps = pd.read_csv(
        os.path.join(BASE_PATH, "fairness/unified_syntax_fairness.csv"), header=None
    )

    # Define the patterns
    pattern_to_remove = re.compile(r"\n\\?|\"|\\n\\?|<font.*?>|\\>|</font>| n ")
    pattern_to_replace = re.compile(r"(SUB:|OBJ:|ASM:|PLN:)(。|：。|：|\)|\)。|）)")
    pattern_X = re.compile(r"X: SUB:")
    undesired_row_pattern = re.compile(
        r"ＨｂASM|SUB:.*SUB:|OBJ:.*OBJ:|ASM:.*ASM:|PLN:.*PLN:|SUB: OBJ: ASM: PLN:|soap|^(?!.*ASM:).*|^(?!.*OBJ:).*"
    )

    # Apply the cleaning function to the 'soap' column
    cleaned_soaps["soap"] = unified_df["soap"].apply(clean_text)

    cleaned_soaps.drop(columns=[cleaned_soaps.columns[-2]], inplace=True)

    cleaned_soaps = remove_rows_with_pattern(
        cleaned_soaps, "soap", undesired_row_pattern
    )

    # Save the cleaned DataFrame to a new CSV file
    cleaned_soaps.to_csv(
        os.path.join(BASE_PATH, "fairness/cleaned_classified_fairness.csv"),
        index=False,
        header=False,
    )

    cleaned_classified_fairness_path = os.path.join(
        BASE_PATH, "fairness/cleaned_classified_fairness.csv"
    )
    output_dir = os.path.join(BASE_PATH, "fairness/soap_sections")

    create_section_csv(cleaned_classified_fairness_path, output_dir)

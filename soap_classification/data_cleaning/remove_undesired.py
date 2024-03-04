import pandas as pd
import re
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps")

# Load the unified syntax SOAP dataset from CSV
unified_soaps = pd.read_csv(
    os.path.join(SOAPS_PATH, "unified_syntax_soap.csv"), header=None
)

# Define the patterns
pattern_to_remove = re.compile(r"\n\\?|\"|\\n\\?|<font.*?>|\\>|</font>")
pattern_to_replace = re.compile(r"(SUB:|OBJ:|ASM:|PLN:)(。|：。|：|\)|\)。|）)")

undesired_row_pattern = re.compile(
    r"ＨｂASM|SUB:.*SUB:|OBJ:.*OBJ:|ASM:.*ASM:|PLN:.*PLN:|SUB: OBJ: ASM: PLN:|soap"
)


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
    return cleaned_text


# Function to remove rows containing a certain pattern
def remove_rows_with_pattern(dataframe, pattern):
    """Removes rows from the DataFrame that contain a specified pattern.

    Args:
        dataframe (DataFrame): The pandas DataFrame from which rows will be removed.
        pattern (str): The pattern to search for within DataFrame rows.

    Returns:
        DataFrame: The modified DataFrame with rows containing the specified pattern removed.
    """
    return dataframe[~dataframe.str.contains(pattern)]


# Apply the cleaning function to the 'soap' column
cleaned_soaps = unified_soaps.iloc[:, 0].apply(clean_text)

cleaned_soaps = remove_rows_with_pattern(cleaned_soaps, undesired_row_pattern)
cleaned_soaps = pd.concat(
    [pd.DataFrame(["Cleaned Classified SOAP Notes"]).T, cleaned_soaps],
    ignore_index=True,
)

# Save the cleaned DataFrame to a new CSV file
cleaned_soaps.to_csv(
    os.path.join(SOAPS_PATH, "cleaned_classified_soaps.csv"), index=False, header=False
)

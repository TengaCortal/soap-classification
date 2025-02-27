import pandas as pd
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps")


def extract_section(soaps_df, section):
    """
    Extracts the specified section from each SOAP note in the DataFrame.

    Args:
    - soaps_df (DataFrame): DataFrame containing SOAP notes.
    - section (str): Section to extract (SUB, OBJ, ASM, or PLN).

    Returns:
    - DataFrame: DataFrame containing only the specified section.
    """
    section_column = []
    for soap in soaps_df["Cleaned Classified SOAP Notes"]:
        start_index = soap.find(section) + len(section) + 1
        if section == "X":
            end_index = soap.find("SUB")
        elif section == "SUB":
            end_index = soap.find("OBJ")
        elif section == "OBJ":
            end_index = soap.find("ASM")
        elif section == "ASM":
            end_index = soap.find("PLN")
        else:
            end_index = len(soap)
        section_text = soap[start_index:end_index].strip()
        section_column.append(section_text)

    section_df = pd.DataFrame({section: section_column})
    return section_df


def create_section_csv(cleaned_classified_soaps_path, output_dir):
    """
    Creates separate CSV files for each section (SUB, OBJ, ASM, and PLN) from the cleaned and classified SOAP notes.

    Args:
    - cleaned_classified_soaps_path (str): Path to the cleaned and classified SOAP notes CSV file.
    - output_dir (str): Directory to save the section CSV files.
    """
    # Read the cleaned and classified SOAP notes CSV file
    soaps_df = pd.read_csv(cleaned_classified_soaps_path)
    # Extract and save each section as a separate CSV file
    sections = ["X", "SUB", "OBJ", "ASM", "PLN"]
    for section in sections:
        section_df = extract_section(soaps_df, section)
        output_path = os.path.join(output_dir, f"{section.lower()}_sections.csv")
        section_df.to_csv(output_path, index=False)
        print(f"{section} section CSV file saved to: {output_path}")

    # Remove all double quotes from each CSV file
    for section in sections:
        output_path = os.path.join(output_dir, f"{section.lower()}_sections.csv")
        with open(output_path, "r") as file:
            lines = file.readlines()
        with open(output_path, "w") as file:
            for line in lines:
                line = line.replace('"', "")
                line = line.replace(",", "")
                # Write line only if it's not empty
                if line.strip():
                    file.write(line)


if __name__ == "__main__":
    cleaned_classified_soaps_path = os.path.join(
        SOAPS_PATH, "cleaned_classified_soaps.csv"
    )
    output_dir = os.path.join(SOAPS_PATH, "soap_sections")

    create_section_csv(cleaned_classified_soaps_path, output_dir)

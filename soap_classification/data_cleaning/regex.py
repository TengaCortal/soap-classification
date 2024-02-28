import csv
import re
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps/by_clinic")

if __name__ == "__main__":
    # Define the regex pattern
    pattern = re.compile(
        r'(?=(。S\)| S。|。S）|。S  |"S|S:|\(S\)|（S）|nS|S：|"S。|。S。|S\.|Ｓ|Ｓ）|<S>|S\))).*(?=(。O\)| O。|。O）|。O |O:|\(O\)|（O）|nO|O：|。O。|O\.|Ｏ|Ｏ）|<O>|O\))).*(?=(。A\)| A。|。A）|。A |A:|\(A\)|（A）|nA|A：|。A。|A\.|Ａ|Ａ）|<A>|A\))).*(?=(。P\)| P。|。P）|。P |P:|\(P\)|（P）|nP|P：|。P。|P\.|Ｐ|Ｐ）|<P>|P\)))'
    )

    # Open the CSV file for reading
    with open(os.path.join(SOAPS_PATH, "yoyogi_soap.csv"), newline="") as csvfile:
        # Initialize a counter for matching rows
        count = 0

        # Create a CSV reader object
        reader = csv.reader(csvfile)

        # Iterate through each row in the CSV file
        for row in reader:
            # Join the row elements into a single string
            row_str = ",".join(row)

            # Check if the regex pattern is in the row
            if pattern.search(row_str):
                # Increment the counter if there's a match
                count += 1

    # Print the number of rows containing the regex pattern
    print("Number of rows containing the regex pattern:", count)

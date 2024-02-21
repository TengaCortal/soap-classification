import csv
import re
import os 

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOAPS_PATH = os.path.join(BASE_PATH, "resources/soaps")

# Define the regex pattern 
pattern = re.compile(r'(?=(。S\)| S。|。S）|。S  |"S|S:|\(S\)|（S）|nS|S：|"S。|。S。|S\.|Ｓ|Ｓ）|<S>|S\))).*(?=(。O\)| O。|。O）|。O |O:|\(O\)|（O）|nO|O：|。O。|O\.|Ｏ|Ｏ）|<O>|O\))).*(?=(。A\)| A。|。A）|。A |A:|\(A\)|（A）|nA|A：|。A。|A\.|Ａ|Ａ）|<A>|A\))).*(?=(。P\)| P。|。P）|。P |P:|\(P\)|（P）|nP|P：|。P。|P\.|Ｐ|Ｐ）|<P>|P\)))')


# Open the combined CSV file
with open(os.path.join(SOAPS_PATH, "combined_soaps.csv"), 'r') as csvfile:
    # Create a CSV reader object
    reader = csv.reader(csvfile)
    
    # Initialize a list to store rows matching the pattern
    matched_rows = []
    
    # Iterate through each row in the CSV file
    for row in reader:
        # Join the row elements into a single string
        row_str = ','.join(row)
        
        # Check if the regex pattern is in the row
        if pattern.search(row_str):
            # If the pattern is found, append the row to the list
            matched_rows.append(row)

# Write the matched rows to a new CSV file
with open('./classified_soaps.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    
    # Write the matched rows to the new CSV file
    writer.writerows(matched_rows)

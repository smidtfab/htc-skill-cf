#!/usr/bin/env python3
import csv
import sys

def convert_abbreviations_to_ids(input_csv: str, output_csv: str) -> None:
    """
    Reads a CSV with columns: text, CF, IC, skill
    Outputs a CSV with columns: text, CF_id, IC_id, skill_id
    """

    # 1. Define your mappings
    cf_map = {
        "B": 1,   # Bond
        "GA": 2,  # Goal alignment
        "TA": 3   # Task agreement
    }

    ic_map = {
        "EAR": 4,
        "CP": 5
    }

    skill_map = {
        "RL": 6,  # Reflective Listening
        "G": 7,   # Genuineness
        "V": 8,   # Validation
        "A": 9,   # Affirmation
        "RA": 10,  # Respect for Autonomy
        "AP": 11,  # Asking for Permission
        "OQ": 12  # Open-ended Question
    }

    # 2. Open the input CSV for reading and the output CSV for writing
    with open(input_csv, mode='r', encoding='utf-8-sig') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        
        # We will write out these columns: text, CF_id, IC_id, skill_id
        fieldnames = ["id", "text", "CF", "CF_id", "IC", "IC_id", "skill", "skill_id"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            example_id = reader.line_num - 1 + 12 # start from 12 ie after the last skill id
            text = row.get("text", "")
            cf_abbrev = row.get("CF", "")
            ic_abbrev = row.get("IC", "")
            skill_abbrev = row.get("skill", "")
            
            # 3. Convert abbreviations to IDs.
            #    If an abbreviation isn't found, you might use a default or raise an error.
            cf_id = cf_map.get(cf_abbrev, "")
            ic_id = ic_map.get(ic_abbrev, "")
            skill_id = skill_map.get(skill_abbrev, "")
            
            # 4. Write the transformed row
            writer.writerow({
                "id": example_id,
                "text": text,
                "CF": cf_abbrev,
                "CF_id": cf_id,
                "IC": ic_abbrev,
                "IC_id": ic_id,
                "skill": skill_abbrev,
                "skill_id": skill_id
            })

def main():
    if len(sys.argv) != 3:
        print("Usage: python convert_abbrev_to_ids.py <input_csv> <output_csv>")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    convert_abbreviations_to_ids(input_csv, output_csv)

if __name__ == "__main__":
    main()
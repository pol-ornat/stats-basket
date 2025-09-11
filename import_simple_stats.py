import csv
import re
import os
from datetime import datetime

# Folder containing all player text files
input_folder = "./cerdanyola"
output_file = "cerdanyola.csv"

# List of valid teams to keep
VALID_TEAMS = {
"PROMOVIATGES CBF CERDANYOLA B",
"DIAGONAL MAR FRONT MARITIM NEGRE",
"ARBRE TEAM - CB IGUALADA SFB",
"CÀMPING BIANYA ROSER B",
"BASQUET NEUS A",
"U.E. CLARET A",
"GRAMENET BC",
"CB IPSI A",
"DRAFT GRAMENET",
"FC MARTINENC BÀSQUET A",
"TIR BAGES - C.B ESPARREGUERA",
"JOVENTUT LES CORTS GROC",
"EL MASNOU BASQUETBOL",
"CB BLANES A",
"ODONTOMED JET TERRASSA",
"U.E. HORTA"
}

# Prepare CSV headers
headers = ["PLAYER", "ROUND", "OPPONENT NAME", "PTS", "MIN", "FOULS", "TL MADE", "TL ATTEMPTED", "2PT MADE", "3PT MADE"]

# Helper function to extract made/attempted from lines like "1/11"
def parse_made_attempted(line):
    if "/" in line:
        made, attempted = line.split("/")
        return int(made), int(attempted)
    return 0, 0

rows = []

# Loop through all text files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        input_file = os.path.join(input_folder, filename)

        # Extract player name from file name
        player_name = os.path.splitext(filename)[0].replace("_", " ").title()

        with open(input_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]

            i = 0
            while i < len(lines):
                opponent = lines[i]

                # Skip games against teams not in the list
                if opponent not in VALID_TEAMS:
                    i += 11
                    continue

                date_time_str = lines[i+1]
                date_obj = datetime.strptime(date_time_str, "%d/%m/%Y %H:%M")

                pts = int(lines[i+2])
                minutes = int(lines[i+3])
                fouls = int(lines[i+4])

                # Free throws
                ft_pct = lines[i+5]     # not used
                ft_made, ft_attempted = parse_made_attempted(lines[i+6])

                # 2PT
                twopt_pct = lines[i+7]  # not used
                twopt_made, _ = parse_made_attempted(lines[i+8])

                # 3PT
                print(filename)
                threept_pct = lines[i+9]  # not used
                threept_made, _ = parse_made_attempted(lines[i+10])

                rows.append([player_name, None, date_obj, opponent, pts, minutes, fouls, ft_made, ft_attempted, twopt_made, threept_made])

                i += 11  # jump to next block

# Sort all rows by date
rows.sort(key=lambda x: x[2])

# Assign round numbers: all games on the same date share the same round
round_number = 0
last_date = None
for row in rows:
    current_date = row[2].date()
    if current_date != last_date:
        round_number += 1
        last_date = current_date
    row[1] = round_number  # ROUND

# Remove the date column before writing
for row in rows:
    del row[2]

# Write to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"CSV file '{output_file}' generated successfully with rounds assigned!")

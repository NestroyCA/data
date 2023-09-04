import re
import csv
new_list = []
input_file_path = "Liste Nestroy_Stücke_Historisch.csv"
output_file_path = "Nestroy_Stücke_import.csv"

with open(input_file_path, "r") as infile:
    reader = csv.reader(infile)
    _=next(reader)
    for row in reader:
        print(row)
        date = re.match(r"^.+\((.+)\)$", row[1])
        if date:
            date = date.group(1).strip()
        else:
            date = ""
        new_list.append(
            [
                f"play_{row[0].zfill(3)}0", row[0], 
                re.sub(
                    r"\(.*[0-9]*.*\)$",
                    "",
                    row[1].strip()
                ).strip(),
                date
            ]
        )
                
with open(output_file_path, "w") as outf:
    writer = csv.writer(outf)
    writer.writerows(new_list)
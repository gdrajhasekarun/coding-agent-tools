import openpyxl
import os
import json
import sys

try:
    work_dir = os.environ["WORK_DIR"]
    input_filepath = os.path.join(work_dir, "uploaded_file.xlsx")

    workbook = openpyxl.load_workbook(input_filepath)
    sheet = workbook["Sheet1"]

    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)

    output_filepath = os.path.join(work_dir, "excel_data.json")
    with open(output_filepath, 'w') as f:
        json.dump(data, f)

    print(json.dumps({"excel_file_path": output_filepath}))

except Exception as e:
    print(json.dumps({"error": str(e)}))
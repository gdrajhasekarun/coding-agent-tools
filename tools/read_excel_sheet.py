import os
import sys
import json
import openpyxl

try:
    # Load the previous step's results if available
    prev = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    
    # Define the input file path
    input_file_path = os.environ.get("UPLOADED_FILE_PATH", "uploaded_file.xlsx") # Assuming a default if not set for testing

    # Define the work directory for output
    work_dir = os.environ.get("WORK_DIR")
    if not work_dir:
        raise ValueError("WORK_DIR environment variable not set.")

    # Process the Excel file
    workbook = openpyxl.load_workbook(input_file_path)
    sheet = workbook["Sheet1"]  # Access Sheet1 as specified

    data = []
    header = [cell.value for cell in sheet[1]]  # Assume first row is header

    for row_index in range(2, sheet.max_row + 1):  # Start from the second row
        row_values = [cell.value for cell in sheet[row_index]]
        row_dict = dict(zip(header, row_values))
        data.append(row_dict)

    # Save the results to a JSON file in the work directory
    output_file_path = os.path.join(work_dir, "sheet1_data.json")
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    # Prepare the summary for the next step
    results = {
        "message": "Successfully read data from Sheet1.",
        "output_file": output_file_path,
        "data_rows": len(data)
    }
    print(json.dumps(results))

except FileNotFoundError:
    print(json.dumps({"error": f"Input file not found: {input_file_path}"}))
except KeyError:
    print(json.dumps({"error": "Sheet1 not found in the Excel file."}))
except Exception as e:
    print(json.dumps({"error": str(e)}))

# METADATA: {"description": "Reads all rows from Sheet1 of the uploaded Excel file.", "inputs": [{"name": "uploaded_file_path", "type": "file", "description": "The path to the uploaded Excel file."}], "outputs": [{"name": "sheet1_data.json", "type": "json", "description": "A JSON file containing the data from Sheet1."}], "limitations": "Assumes the uploaded file is a valid Excel (.xlsx) file and Sheet1 exists. Assumes the first row of Sheet1 is the header."}
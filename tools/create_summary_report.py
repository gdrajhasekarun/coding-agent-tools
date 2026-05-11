import os
import sys
import json
import pandas as pd

try:
    # Check if context from previous step is available
    if not sys.stdin.isatty():
        prev_step_data = json.loads(sys.stdin.read())
        if "error" in prev_step_data:
            raise Exception(prev_step_data["error"])
    else:
        # If no previous step data, assume file exists based on the context provided
        # In a real scenario, this might need a more robust way to handle standalone execution
        pass

    work_dir = os.environ.get("WORK_DIR")
    if not work_dir:
        raise Exception("WORK_DIR environment variable not set.")

    # In a real scenario, the filename would likely be passed from a previous step or configuration
    # For this example, we'll assume the filename based on the error from the previous step
    file_path = os.path.join(work_dir, "uploaded_file.xlsx")

    # Read the excel sheet into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Generate a summary report
    summary_report = df.describe().to_json()

    # Save the summary report as a JSON file
    summary_file_path = os.path.join(work_dir, "summary_report.json")
    with open(summary_file_path, 'w') as f:
        f.write(summary_report)

    # Prepare the output for the next step
    output_data = {
        "summary_report_path": summary_file_path
    }

    print(json.dumps(output_data))

except Exception as e:
    print(json.dumps({"error": str(e)}))

# METADATA: {"description": "Generate a summary report from the DataFrame.", "inputs": [{"name": "previous_step_output", "type": "json", "description": "Output from the previous step (e.g., file path to excel)."}], "outputs": [{"name": "summary_report_path", "type": "json", "description": "Path to the generated JSON summary report."}], "limitations": "Assumes the input file 'uploaded_file.xlsx' exists in the WORK_DIR. Error handling for file not found is present."}
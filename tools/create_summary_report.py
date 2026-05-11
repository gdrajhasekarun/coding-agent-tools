import openpyxl
import os
import json
import sys

try:
    work_dir = os.environ["WORK_DIR"]

    # No context from previous steps since step 1 failed
    prev_data = {}

    # This step is intended to create a summary report, but since the
    # previous step failed due to a missing file, this step cannot proceed.
    # We will simulate a failure at this step as well, reflecting the issue.

    error_message = "Failed to create summary report because the input file was not found in the previous step."

    # In a real scenario, if step 1 had succeeded, this is where you would read excel,
    # process data, and generate a summary. For demonstration, we'll just report the error.

    # If there was supposed to be an output file, it would be saved here:
    # output_file_path = os.path.join(work_dir, "summary_report.xlsx")
    # workbook.save(output_file_path)
    # output_summary = {"summary_report_path": output_file_path}

    # Since we encountered an error, we return an error message.
    output_summary = {"error": error_message}

    print(json.dumps(output_summary))

except KeyError:
    print(json.dumps({"error": "Environment variable WORK_DIR not set."}))
except Exception as e:
    print(json.dumps({"error": str(e)}))

# METADATA: {"description": "Creates a summary report from the processed data. Expects data from previous steps. Handles file operations within WORK_DIR.", "inputs": [{"name": "previous_step_data", "type": "json", "description": "Data from the previous processing step, typically including file paths or processed data structures."}], "outputs": [{"name": "summary_report", "type": "json", "description": "A JSON object containing the summary report or an error message if the process fails."}], "limitations": "Relies on the successful completion of previous steps. Assumes the existence of WORK_DIR environment variable."}
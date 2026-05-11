import pandas as pd
import json
import os

try:
    # Check if a previous step provided input DataFrame
    try:
        import sys
        prev = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
        if "df" in prev:
            df = pd.DataFrame(prev["df"])
        else:
            raise KeyError("No 'df' key found in previous step's output.")
        if "file_path" in prev:
            file_path = prev["file_path"]
        else:
            raise KeyError("No 'file_path' key found in previous step's output.")
    except Exception as e:
        raise ValueError(f"Failed to load data from previous step: {e}")

    # Get the work directory
    work_dir = os.environ.get("WORK_DIR")
    if not work_dir:
        raise ValueError("WORK_DIR environment variable not set.")

    # Create a summary report
    summary = df.describe().to_json()
    summary_file_path = os.path.join(work_dir, "summary_report.json")
    with open(summary_file_path, "w") as f:
        f.write(summary)

    # Prepare the output JSON
    output_data = {
        "summary_report_path": summary_file_path,
        "message": "Summary report created successfully."
    }

    # Print the output JSON to stdout
    print(json.dumps(output_data))

except Exception as e:
    # Print error message to stdout if an error occurs
    print(json.dumps({"error": str(e)}))

# METADATA: {"description": "Creates a summary report (descriptive statistics) from a DataFrame.", "inputs": [{"name": "df", "type": "pandas.DataFrame"}, {"name": "file_path", "type": "str"}], "outputs": [{"name": "summary_report_path", "type": "str", "description": "Path to the generated JSON summary report."}], "limitations": "Requires a pandas DataFrame as input. Assumes the DataFrame is already loaded and available from a previous step."}
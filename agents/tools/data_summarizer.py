import os
import json
import pandas as pd

def main():
    try:
        # Read previous context if available
        prev = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}

        # Load the uploaded input file path from environment variables
        uploaded_file_path = os.environ.get("UPLOADED_FILE_PATH")
        if not uploaded_file_path:
            raise FileNotFoundError("Uploaded file path is not set in environment variables.")
        
        # Load the data
        data = pd.read_excel(uploaded_file_path)

        # Summarize the data (for example, calculate means of numerical columns)
        summary = data.describe().to_dict()

        # Prepare output directory
        work_dir = os.environ.get("WORK_DIR")
        if not work_dir:
            raise FileNotFoundError("Working directory is not set in environment variables.")
        
        # Save the summary as a JSON file in the working directory
        summary_file_path = os.path.join(work_dir, "summary.json")
        with open(summary_file_path, "w") as summary_file:
            json.dump(summary, summary_file)

        # Print summary to stdout for the next step
        print(json.dumps({"summary": summary}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))

# Entry point
if __name__ == "__main__":
    main()
# METADATA: {"description": "Generates a summary from an uploaded Excel file.", "inputs": ["UPLOADED_FILE_PATH"], "outputs": ["summary.json"], "limitations": "Assumes uploaded file is a valid Excel file and exists."}
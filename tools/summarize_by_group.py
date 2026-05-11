import pandas as pd
import json
import os

try:
    work_dir = os.environ["WORK_DIR"]
    input_file = os.path.join(work_dir, 'uploaded_file.xlsx')

    # Check if the input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found at {input_file}")

    df = pd.read_excel(input_file)

    # Ensure necessary columns exist
    required_columns = ['Category', 'Sales', 'Quantity']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convert 'Sales' and 'Quantity' to numeric, coercing errors to NaN
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

    # Drop rows where 'Sales' or 'Quantity' became NaN after coercion
    df.dropna(subset=['Sales', 'Quantity'], inplace=True)

    # Group by 'Category' and aggregate
    summary_df = df.groupby('Category').agg(
        Total_Sales=('Sales', 'sum'),
        Number_of_Sales=('Sales', 'count'),
        Total_Quantity=('Quantity', 'sum')
    ).reset_index()

    summary_file_path = os.path.join(work_dir, 'group_summary.json')
    summary_df.to_json(summary_file_path, orient='records')

    # Prepare output for stdout
    output_summary = {
        "summary_file": os.path.basename(summary_file_path),
        "status": "success"
    }
    print(json.dumps(output_summary))

except FileNotFoundError as e:
    print(json.dumps({"error": str(e)}))
except ValueError as e:
    print(json.dumps({"error": str(e)}))
except Exception as e:
    print(json.dumps({"error": f"An unexpected error occurred: {str(e)}"}))

# METADATA: {"description": "Summarize the data by grouping rows by 'Category' and aggregating numerical columns ('Sales', 'Quantity') using sum and count respectively.", "inputs": [{"name": "uploaded_file.xlsx", "type": "excel"}], "outputs": [{"name": "group_summary.json", "type": "json"}], "limitations": "Assumes the Excel file has sheets that can be read and contains 'Category', 'Sales', and 'Quantity' columns. Numerical columns will be coerced to numeric types; any values that cannot be converted will result in those rows being excluded from aggregation."}
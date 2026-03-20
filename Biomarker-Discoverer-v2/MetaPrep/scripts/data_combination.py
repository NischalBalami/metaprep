"""
Third Step
Takes all the grouped sample files and stacks them into
one big spreadsheet, tagging each row with which sample it came from
"""
import pandas as pd
import glob
import os


def combine_grouped_files(grouped_folder, output_folder):
    files = glob.glob(os.path.join(grouped_folder, "*.xlsx"))
    if not files:
        print(f"No grouped files found in {grouped_folder}.")
        return

    combined_data = []
    for file in files:
        data = pd.read_excel(file)
        if data.empty:
            print(f"Skipping empty file: {file}")
            continue

        required_cols = ['basePeakMz', 'retentionTime', 'summedIntensity']
        if not all(col in data.columns for col in required_cols):
            print(f"Skipping {file} (missing required columns).")
            continue

        data = data[required_cols]
        data['SourceFile'] = os.path.basename(file)
        combined_data.append(data)

    if not combined_data:
        print("No valid grouped files to combine.")
        return

    combined_data = pd.concat(combined_data, ignore_index=True)
    os.makedirs(output_folder, exist_ok=True)

    combined_file = os.path.join(output_folder, "combined_data.xlsx")
    combined_data.to_excel(combined_file, index=False)
    print(f"Combined file created at: {combined_file}")

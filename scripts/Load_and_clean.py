"""
First Step
Reads raw peaklist files, drops empty rows, fixes column names
so everything is consistent, and cleans up retention time values
"""
import os
import pandas as pd
import glob


def clean_data(file_path, processed_folder):
    print(f"Processing file: {file_path}")
    data = pd.read_excel(file_path)
    data = data.dropna()

    # Standardize column names
    col_map = {col.lower(): col for col in data.columns}
    mz_col = col_map.get("mz", "basePeakMz")
    rt_col = col_map.get("rt", "retentionTime")
    pa_col = col_map.get("pa", "basePeakIntensity")

    data = data.rename(columns={
        mz_col: "basePeakMz",
        rt_col: "retentionTime",
        pa_col: "basePeakIntensity"
    })

    # Clean RT column (remove PT/S if present)
    if "retentionTime" in data.columns:
        data["retentionTime"] = (
            data["retentionTime"].astype(str)
            .str.replace("PT", "", regex=False)
            .str.replace("S", "", regex=False)
        )
        data["retentionTime"] = pd.to_numeric(data["retentionTime"], errors="coerce")

    # Save cleaned file
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    processed_filename = f"{name}_processed{ext}"
    processed_path = os.path.join(processed_folder, processed_filename)

    os.makedirs(processed_folder, exist_ok=True)
    data.to_excel(processed_path, index=False)
    print(f"Saved cleaned file to: {processed_path}")


def process_all_files(raw_folder, processed_folder):
    files = glob.glob(os.path.join(raw_folder, "*.xlsx"))
    if not files:
        print(f"No raw data files found in {raw_folder}.")
        return
    for file_path in files:
        clean_data(file_path, processed_folder)

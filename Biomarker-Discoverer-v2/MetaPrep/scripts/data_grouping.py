"""
Second Step
Groups nearby peaks that are probably the same molecule
If two peaks have similar m/z and RT, they get merged into one and their intensities are added together
"""
import pandas as pd
import numpy as np
import os


def group_peaks(data, mz_threshold, rt_threshold):
    grouped_data = []

    # Ensure required columns
    required_cols = ["basePeakMz", "retentionTime", "basePeakIntensity"]
    if not all(col in data.columns for col in required_cols):
        print("Missing required columns. Skipping file.")
        return pd.DataFrame()

    # Sort for consistency
    data = data.sort_values(by=["basePeakMz", "retentionTime"])
    grouped_flags = np.zeros(len(data), dtype=bool)

    for i, row in data.iterrows():
        if grouped_flags[i]:
            continue

        mz, rt, pa = row["basePeakMz"], row["retentionTime"], row["basePeakIntensity"]

        within_threshold = (
            (np.abs(data["basePeakMz"] - mz) <= mz_threshold) &
            (np.abs(data["retentionTime"] - rt) <= rt_threshold)
        )

        matching_indices = data[within_threshold].index
        total_pa = data.loc[matching_indices, "basePeakIntensity"].sum()

        grouped_peak = {"basePeakMz": mz, "retentionTime": rt, "summedIntensity": total_pa}
        grouped_data.append(grouped_peak)

        grouped_flags[matching_indices] = True

    return pd.DataFrame(grouped_data)


def process_grouping(processed_folder, output_folder, mz_threshold, rt_threshold):
    files = [f for f in os.listdir(processed_folder) if f.endswith(".xlsx")]
    if not files:
        print(f"No processed files in {processed_folder}")
        return

    os.makedirs(output_folder, exist_ok=True)

    for file in files:
        file_path = os.path.join(processed_folder, file)
        print(f"Grouping peaks in: {file}")

        data = pd.read_excel(file_path)
        grouped_data = group_peaks(data, mz_threshold, rt_threshold)

        if grouped_data.empty:
            print(f"Warning: {file} produced empty grouped file.")
            continue

        grouped_filename = f"{os.path.splitext(file)[0]}_grouped.xlsx"
        grouped_file_path = os.path.join(output_folder, grouped_filename)

        grouped_data.to_excel(grouped_file_path, index=False)
        print(f"Grouped file saved to: {grouped_file_path}")

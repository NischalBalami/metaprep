"""
Fourth Step
Builds the final comparison table - each row is a unique molecule, each column shows how much of it was found in each sample
This is what you use to spot differences between groups
"""
import pandas as pd
import numpy as np
import os


def cross_sample_alignment(combined_file, output_folder, mz_threshold, rt_threshold):
    print(f"Loading combined data from: {combined_file}")
    data = pd.read_excel(combined_file)

    required_cols = ['basePeakMz', 'retentionTime', 'summedIntensity', 'SourceFile']
    if not all(col in data.columns for col in required_cols):
        print(f"Error: Combined file missing required columns.")
        return

    samples = data['SourceFile'].unique()
    print(f"Samples detected: {samples}")

    feature_table = pd.DataFrame(columns=['mz', 'rt'] + [f'pa_{s}' for s in samples])

    for _, row in data.iterrows():
        mz, rt, pa, sample = row['basePeakMz'], row['retentionTime'], row['summedIntensity'], row['SourceFile']

        if not feature_table.empty:
            mz_diff = np.abs(feature_table['mz'] - mz) <= mz_threshold
            rt_diff = np.abs(feature_table['rt'] - rt) <= rt_threshold
            match = feature_table[mz_diff & rt_diff]
        else:
            match = pd.DataFrame()

        if not match.empty:
            idx = match.index[0]
            feature_table.at[idx, f'pa_{sample}'] += pa
        else:
            new_row = {'mz': mz, 'rt': rt}
            for s in samples:
                new_row[f'pa_{s}'] = 0
            new_row[f'pa_{sample}'] = pa
            feature_table = pd.concat([feature_table, pd.DataFrame([new_row])], ignore_index=True)

    feature_table.fillna(0, inplace=True)

    os.makedirs(output_folder, exist_ok=True)
    aligned_file = os.path.join(output_folder, "aligned_file.xlsx")
    feature_table.to_excel(aligned_file, index=False)

    print(f"Cross-sample alignment saved at: {aligned_file}")

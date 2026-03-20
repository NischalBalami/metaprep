"""
Biomarker Discoverer - Automated Pipeline Runner
Runs all 4 stages of the pipeline using default paths and thresholds.
Usage: cd scripts && python run_pipeline.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from Load_and_clean import process_all_files
from data_grouping import process_grouping
from data_combination import combine_grouped_files
from cross_sample_alignment import cross_sample_alignment

# Paths (relative to project root)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_FOLDER = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "data", "processed")
GROUPED_FOLDER = os.path.join(BASE_DIR, "data", "grouped")
COMBINED_FOLDER = os.path.join(BASE_DIR, "data", "combined")
ALIGNED_FOLDER = os.path.join(BASE_DIR, "data", "aligned")

# Default thresholds
MZ_THRESHOLD = 0.001
RT_THRESHOLD = 30


def main():
    print("=" * 60)
    print("BIOMARKER DISCOVERER - FULL PIPELINE")
    print("=" * 60)
    print(f"MZ threshold: {MZ_THRESHOLD}")
    print(f"RT threshold: {RT_THRESHOLD} seconds")

    # Step 1: Clean raw data
    print("\n>>> STEP 1: Cleaning raw data files...")
    print("-" * 40)
    process_all_files(RAW_FOLDER, PROCESSED_FOLDER)

    # Step 2: Group peaks
    print("\n>>> STEP 2: Grouping peaks...")
    print("-" * 40)
    process_grouping(PROCESSED_FOLDER, GROUPED_FOLDER, MZ_THRESHOLD, RT_THRESHOLD)

    # Step 3: Combine grouped files
    print("\n>>> STEP 3: Combining grouped files...")
    print("-" * 40)
    combine_grouped_files(GROUPED_FOLDER, COMBINED_FOLDER)

    # Step 4: Cross-sample alignment
    print("\n>>> STEP 4: Aligning across samples...")
    print("-" * 40)
    combined_file = os.path.join(COMBINED_FOLDER, "combined_data.xlsx")
    cross_sample_alignment(combined_file, ALIGNED_FOLDER, MZ_THRESHOLD, RT_THRESHOLD)

    # Summary
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE!")
    print("=" * 60)
    print("\nOutput files:")
    for folder_name, folder_path in [
        ("Processed", PROCESSED_FOLDER),
        ("Grouped", GROUPED_FOLDER),
        ("Combined", COMBINED_FOLDER),
        ("Aligned", ALIGNED_FOLDER),
    ]:
        if os.path.exists(folder_path):
            files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]
            for f in files:
                fpath = os.path.join(folder_path, f)
                size = os.path.getsize(fpath)
                print(f"  [{folder_name}] {f} ({size:,} bytes)")


if __name__ == "__main__":
    main()

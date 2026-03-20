"""
Biomarker Discoverer - Interactive Pipeline Runner
Provides a menu-driven interface to run each pipeline step
with custom folder paths and threshold parameters.
"""
from Load_and_clean import process_all_files
from data_grouping import process_grouping
from data_combination import combine_grouped_files
from cross_sample_alignment import cross_sample_alignment
import os


def get_valid_path(prompt):
    while True:
        path = input(prompt)
        if os.path.exists(path):
            return path
        else:
            print("Invalid path. Try again.")


if __name__ == "__main__":
    print("Welcome to the Biomarker Data Pipeline!")

    while True:
        print("\nOptions:")
        print("1. Clean raw data files")
        print("2. Group peaks in processed files")
        print("3. Combine grouped files")
        print("4. Align grouped files across samples")
        print("5. Exit")

        action = input("Select an action (1-5): ")

        if action == '1':
            raw_folder = get_valid_path("Enter raw data folder: ")
            processed_folder = input("Enter folder to save processed files: ")
            process_all_files(raw_folder, processed_folder)

        elif action == '2':
            processed_folder = get_valid_path("Enter processed folder: ")
            output_folder = input("Enter folder to save grouped files: ")
            mz_threshold = float(input("Enter MZ threshold (e.g., 0.001): "))
            rt_threshold = float(input("Enter RT threshold (seconds, e.g., 30): "))
            process_grouping(processed_folder, output_folder, mz_threshold, rt_threshold)

        elif action == '3':
            grouped_folder = get_valid_path("Enter grouped folder: ")
            output_folder = input("Enter folder to save combined file: ")
            combine_grouped_files(grouped_folder, output_folder)


        elif action == '4':
            combined_path = get_valid_path("Enter combined data folder or file path: ")
            # If user provides a folder, look for combined_data.xlsx inside it
            if os.path.isdir(combined_path):
                combined_file = os.path.join(combined_path, "combined_data.xlsx")
                if not os.path.exists(combined_file):
                    print(f"Error: combined_data.xlsx not found in {combined_path}")
                    continue

            else:
                combined_file = combined_path
            aligned_folder = input("Enter folder to save aligned file: ")
            mz_threshold = float(input("Enter MZ threshold (e.g., 0.001): "))
            rt_threshold = float(input("Enter RT threshold (seconds, e.g., 30): "))
            cross_sample_alignment(combined_file, aligned_folder, mz_threshold, rt_threshold)

        elif action == '5':
            print("Exiting pipeline. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

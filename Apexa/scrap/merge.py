import pandas as pd
import glob

def merge_csv_files(input_folder, output_file):
    """
    Merges all CSV files in a given folder into a single CSV file,
    keeping all unique columns and filling missing values with NaN.
    
    :param input_folder: Path to the folder containing CSV files.
    :param output_file: Path to save the merged CSV file.
    """
    # Get all CSV file paths from the folder
    file_paths = glob.glob(rf"{input_folder}\*.csv")  # Use raw string (r) to avoid escape issues
    
    # Read all CSV files into DataFrames
    dfs = [pd.read_csv(file) for file in file_paths]
    
    # Merge all DataFrames, keeping all unique columns
    merged_df = pd.concat(dfs, ignore_index=True, sort=False)
    
    # Save the merged DataFrame to a CSV file
    merged_df.to_csv(output_file, index=False)
    
    print(f"Merged {len(file_paths)} files into {output_file}")

# Example usage
merge_csv_files(r"C:\Users\sachi\Desktop\Apexa\scrap", "merged_output.csv")

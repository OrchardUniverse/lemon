#!/usr/bin/env python

import sys
import pandas as pd


seperator = ','
#seperator = '|'
def convert_file(input_path: str, output_path: str):
    """
    Converts a CSV file to Excel or an Excel file to CSV based on the input and output file extensions.

    :param input_path: Path to the input file (CSV or Excel).
    :param output_path: Path to the output file (Excel or CSV).
    """
    if input_path.endswith('.csv') and output_path.endswith('.xlsx'):
        # Convert CSV to Excel
        df = pd.read_csv(input_path, sep=seperator)
        df.to_excel(output_path, index=False)
        print(f"CSV file '{input_path}' has been converted to Excel file '{output_path}'.")

    elif input_path.endswith('.xlsx') and output_path.endswith('.csv'):
        # Convert Excel to CSV
        df = pd.read_excel(input_path)
        df.to_csv(output_path, sep=seperator, index=False)
        print(f"Excel file '{input_path}' has been converted to CSV file '{output_path}'.")
        
    else:
        print("Invalid file extensions. Please ensure you are converting between CSV and Excel files.")

# Example usage:

def main():
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_file(input_file, output_file)
    else:
        print("Not enough arguments provided. Please provide input file and output file.")

if __name__ == "__main__":
  main()

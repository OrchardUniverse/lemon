#!/usr/bin/env python

import csv
import os

# Configuration
output_csv = 'test_data.csv'
num_rows = 100
delimiter = '|'

# CSV data generation
header = ['index', 'question', 'groundtruth', 'answer']
data = [
    (i, f'Test Question {i}?', f'Ground Truth {i}', f'Answer {i}') for i in range(num_rows)
]

# Path check and CSV writing
if not os.path.isfile(output_csv):
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=delimiter)
        writer.writerow(header)
        writer.writerows(data)
    print(f'CSV file {output_csv} has been created with {num_rows} rows.')
else:
    print(f'File {output_csv} already exists.')
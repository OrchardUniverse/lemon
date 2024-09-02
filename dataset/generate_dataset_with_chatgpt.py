#!/usr/bin/env python

import csv
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_util import call_llm

# Output file name
output_filename = 'dataset.csv'
#output_filename = 'dataset_test.csv'

# Generate sample data for the CSV
sample_data = [
    {'index': i, 'question': f'Test question {i}', 'groundtruth': f'Test ground truth {i}'}
    for i in range(3)
]


# Add answers from ChatGPT
for item in sample_data:
    item['question'] = call_llm("Generate a simple common-sense question and only output the question.")
    print(f"Generate a simple question: {item['question']}")

    item['groundtruth'] = call_llm(f"Anser the question sipmly: {item['question']}")
    print(f"Generate a ground truth answer: {item['groundtruth']}")

    item['answer'] = call_llm(f"Anser the question sipmly: {item['question']}")
    print(f"Generate a answer: {item['answer']}")


# Write the data to a CSV file
with open(output_filename, 'w', newline='') as csvfile:
    fieldnames = ['index', 'question', 'groundtruth', 'answer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')

    # Write header
    writer.writeheader()

    # Write rows
    for row in sample_data:
        writer.writerow(row)

print(f'CSV file {output_filename} has been created with sample data.')

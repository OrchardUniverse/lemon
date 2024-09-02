#!/usr/bin/env python

import csv
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge
import sys
import os
import openpyxl

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from llm_util import call_llm

input_dataset_file = "../dataset/dataset.csv"
#input_dataset_file = "../dataset/dataset.xlsx"

model_score_prompt = """
Evaluate the accuracy of the following user answer in comparison to the provided ground truth. Rate the accuracy on a scale from 0 to 10, where 0 means the user's answer is completely incorrect or irrelevant, and 10 means it is exactly the same as the ground truth. Consider accuracy, completeness, and relevance in your evaluation.
Only output the rating score and do not output extra information like explanation.

Ground Truth: {ground_truth}

User's Answer: {answer}

Rating (0-10):
"""

def calculate_model_score(ground_truth, answer):
    prompt = model_score_prompt.format(ground_truth=ground_truth, answer=answer)
    response = call_llm(prompt)
    try:
        print(f"Call llm to get the model rating score: {response}")
        return int(response)
    except ValueError:
        print(f"Fail to parse the model score from the response: {response}")
        exit(0)



# Function to calculate BLEU score
def calculate_bleu(reference, candidate):
    return sentence_bleu([reference.split()], candidate.split(), weights=(0.25, 0.25, 0.25, 0.25))

# Function to calculate ROUGE scores
def calculate_rouge(reference, candidate):
    rouge = Rouge()
    scores = rouge.get_scores(candidate, reference)[0]
    return scores['rouge-1']['f'], scores['rouge-2']['f']


def evaluate_csv_file(input_dataset_file):
    # Read the dataset CSV file
    with open(input_dataset_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        next(reader)  # Skip the header

        # Prepare the results list
        results = []

        for row in reader:
            index, question, ground_truth, answer = row
            blue = calculate_bleu(ground_truth, answer)
            rouge_1, rouge_2 = calculate_rouge(ground_truth, answer)
            model_rating = calculate_model_score(ground_truth, answer)

            results.append({'index': index, 'blue': blue, 'rouge-1': rouge_1, 'rouge-2': rouge_2, 'model_rating': model_rating})
        
        return results



def evaluate_excel_file(input_dataset_file):

    wb = openpyxl.load_workbook(input_dataset_file)
    ws = wb.active

    # Prepare the results list
    results = []
    for row in ws.iter_rows(min_row=2, values_only=True):  # Skip the header
        index, question, ground_truth, answer = row

        blue = calculate_bleu(ground_truth, answer)
        rouge_1, rouge_2 = calculate_rouge(ground_truth, answer)
        model_rating = calculate_model_score(ground_truth, answer)
        results.append({'index': index, 'blue': blue, 'rouge-1': rouge_1, 'rouge-2': rouge_2, 'model_rating': model_rating})

    return results


results = evaluate_csv_file(input_dataset_file)
#results = evaluate_excel_file(input_dataset_file)

# Write the metrics to a CSV file
def write_metrics_to_csv(metrics):
    with open('metrics.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['index', 'blue', 'rouge-1', 'rouge-2', 'model_rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in metrics:
            writer.writerow(data)

write_metrics_to_csv(results)

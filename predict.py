import torch
import numpy as np
import pandas as pd
from torch.nn import functional as F
from transformers import BertTokenizer, BertForMaskedLM
import torch
from parser.changeVar import changeVar
from parser.filter import filter_result
from parser.parse import parse
import string

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

import argparse


def predict(code_path, variable):
    with open(code_path, "r", encoding="utf-8") as f:
        method = f.read()
    variables = parse(method)
    variables.remove(variable)

    changed_method = changeVar(method, variable, '[BLANK]')
    flatten_method = changed_method.replace('\n', '').replace('[BLANK]', tokenizer.mask_token)

    input = tokenizer.encode_plus(flatten_method, return_tensors="pt")
    input_cuda = {
        'input_ids': input['input_ids'].cuda(),
        'token_type_ids': input['token_type_ids'].cuda(),
        'attention_mask': input['attention_mask'].cuda()
    }
    output = model(**input_cuda)
    logits = output.logits
    softmax = F.softmax(logits, dim=-1)

    # Find the indices of the masked tokens in the input sequence
    mask_token_indices = torch.where(input_cuda['input_ids'] == tokenizer.mask_token_id)[1]

    # Iterate over each mask token index to get predictions
    top_predictions_per_mask = []
    for mask_index in mask_token_indices:
        # Get the predictions for the current masked token
        masked_token_logits = logits[0, mask_index, :]

        # Pick the top 5 candidate tokens for the masked position
        top_5_candidates = torch.topk(masked_token_logits, k=5, dim=-1)

        # Convert the predicted token IDs to the respective words
        predicted_token_ids = top_5_candidates.indices.tolist()
        predicted_tokens = tokenizer.convert_ids_to_tokens(predicted_token_ids)

        # Save the predictions
        top_predictions_per_mask.append(predicted_tokens)

    # Display the top 5 predictions for each masked token
    # for i, predictions in enumerate(top_predictions_per_mask):
    #     print(f"Mask {i + 1} top predictions: {predictions}")

    valid_variables = filter_result(top_predictions_per_mask, method, variables, variable, 5)

    return list(valid_variables.keys())

# Create the parser
parser = argparse.ArgumentParser(description='Sample argparse Python application.')

# Add arguments
parser.add_argument('-m', '--method_path', type=str)
parser.add_argument('-v', '--variable', type=str)

# Parse the command-line arguments
args = parser.parse_args()


model = torch.load('models/model.pt')
print(predict(args.method_path, args.variable))
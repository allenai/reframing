""" Official evaluation script for DATASET_NAME dataset. """
from __future__ import print_function
from collections import Counter
import string
import re
import argparse
import json
import tqdm
from tqdm import tqdm
import datasets
import numpy as np
from typing import List, Dict
import pandas as pd

bleurt_metric = datasets.load_metric('bleurt', **{'config_name': 'bleurt-base-128'})
rouge_metric = datasets.load_metric('rouge')
sacrebleu_metric = datasets.load_metric('sacrebleu')


def bleurt(prediction: str, ground_truth: str):
    score = bleurt_metric.compute(
        predictions=[prediction],
        references=[ground_truth]
    )
    return np.mean(score['scores'])


def rouge(prediction: str, ground_truth: str):
    score = rouge_metric.compute(
        predictions=[prediction],
        references=[ground_truth],
        **{'use_agregator': False, 'use_stemmer': True, 'rouge_types': ['rougeL']}
    )
    return score['rougeL'][0].fmeasure


def sacrebleu(prediction: str, ground_truth_list: List[str]):
    score = sacrebleu_metric.compute(
        predictions=[prediction],
        references=[ground_truth_list]  # scarebleu expects several golds per
    )
    return score['score'] / 100


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction: str, ground_truth: str):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def exact_match_score(prediction: str, ground_truth: str):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def metric_max_over_ground_truths(metric_fn, prediction: str, ground_truths: List[str]):
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)


def evaluate(dataset: List[str], predictions: List[str], evaluation_types: List[str], dataset_name) -> Dict:
    '''
    :param dataset: json file containing the gold labels
    :param predictions: list of strings, as the predictions
    :param evaluation_types: TODO
    :return:
    '''
    print(len(predictions))
    print(len(dataset))
    # TODO: update this so that the script accepts partial predictions
    assert len(predictions) == len(dataset), \
        f"The pred file does not have the same length as the gold data: {len(dataset)} vs {len(predictions)}"

    metrics = {}
    #max_eval = 10
    for idx, (gold_item, pred) in tqdm(enumerate(zip(dataset, predictions))):

        # hack, to make it easier faster to test this code; drop it later
        #if idx > max_eval:
            #break
        r, b, s, em, f1 = 0, 0, 0, 0, 0
        r_max, b_max, s_max, em_max, f1_max = 0, 0, 0, 0, 0
        max_idx = 0
        for gidx, gold in enumerate(gold_item):
            gold_outputs = gold.split(',')
            
            # long-range text generation metrics
            if "long_generation" in evaluation_types:
                if 'rouge' not in metrics:
                    metrics['sacrebleu'] = metrics['bleurt'] = metrics['rouge'] = 0
                r = metric_max_over_ground_truths(rouge, pred, gold_outputs)
                b = metric_max_over_ground_truths(bleurt, pred, gold_outputs)
                s = sacrebleu(pred, gold_outputs)
    
            # squad-like f1/em metrics
            if "short_answer" in evaluation_types:
                if 'exact_match' not in metrics:
                    metrics['f1'] = metrics['exact_match'] = 0
                em = metric_max_over_ground_truths(exact_match_score, pred, gold_outputs)
                f1 = metric_max_over_ground_truths(f1_score, pred, gold_outputs)
    
            # e.g., selecting A, B, C, etc.
            if "classification" in evaluation_types:
                pass
    
            # TODO: task-specific constraints:
            if "winogrande_question_generation_object" in dataset_name:
                #   e.g., for Winogrande, check if PerxonX comes before PersonY: metrics['personx-before-persony_score'] = ...
                pass
            
            if f1_max < f1:
                f1_max = f1
                r_max = r
                s_max = s
                em_max = em
                b_max = b
                max_idx = gidx
                
        metrics['sacrebleu'] += s_max
        metrics['f1'] += f1_max
        metrics['exact_match'] += em_max
        metrics['bleurt'] += b_max
        metrics['rouge'] += r_max
    
        dataset[idx] = dataset[idx][max_idx]
    
    # normalize tne metrics
    for key in metrics.keys():
        metrics[key] /= len(predictions)

    print(json.dumps(metrics))
    
    file = open(dataset_name[:-5] + "_final.json", "w")
    json.dump({"true": dataset, "prediction": predictions}, file, indent = 4)
    file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluation for DATASET-NAME ')
    parser.add_argument('--dataset_file', help='Dataset file')
    args = parser.parse_args()
    print(args.dataset_file)
    
    
    i = args.dataset_file.find("_")
    # args.dataset_file[:i] + "/" +
    file = open(args.dataset_file, "r")
    data = json.load(file)
    file.close()
    
    
    
    ground_truth = data["true"]
    predictions = data["prediction"]
    
    

    # TODO: read this from the gold data
    # evaluation_types = ['short_answer']
    evaluation_types = ['long_generation', 'short_answer']
    evaluate(ground_truth, predictions, evaluation_types, args.dataset_file)
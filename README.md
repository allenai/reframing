# Reframing Instructional Prompts to GPTk's Language

## Description
This repository contains the code to reproduce results obtained in Figure 2 of [Mishra et. al](https://arxiv.org/pdf/2109.07830.pdf). We use 12 tasks from [NATURAL INSTRUCTIONS v1.1](https://instructions.apps.allenai.org/). The tasks are tabled in Table 2 for [Mishra et. al](https://arxiv.org/pdf/2109.07830.pdf). 

There are two sets of results. The first set, baseline, is obtained from using raw instructions for these tasks. In the second set, we reframe these instructions using techniques described in the paper. We call these results reframed. 

For both results, we use gpt2, gpt2-xl, gpt2large, gpt3 and gpt3 instruct. Both the results are made in few shot setting with 5 positive examples provided each time.

## Raw instructions

Each prompt for raw instructions is defined using the "Definition", "Emphasis & Caution", "Things to Avoid", "Prompt", "Positive Examples Full Only" fields, in that order, from files in Dataset_Jsons.

The script named encodeinstructions outputs the encoded raw instructions.

## Reframed instructions:

All the reframed instructions are present in the README file in reframed_instructions directory.

The script named encodeinstructions_reframed outputs the encoded reframed instructions.

## Hyperparameters:

For both GPT3 and GPT3 instruct, we use the following hyperparameters: 
temperature: 0.7  
top_p = 1  
frequency_penalty = 0  
presence_penalty = 0

We also change the max_token hyperparameter according to the task on hand. 

For the following tasks, we set it to 3.\
'subtask022_cosmosqa_passage_inappropriate_binary'  
'subtask005_mctaco_wrong_answer_generation_event_duration' 'subtask008_mctaco_wrong_answer_generation_transient_stationary'  
'subtask033_winogrande_answer_generation'  
'subtask039_qasc_find_overlapping_words'  
'subtask052_multirc_identify_bad_question'  

For the following tasks, we set it to 10:  
'subtask044_essential_terms_identifying_essential_words'  
'subtask002_quoref_answer_generation'  

For the following tasks, we set it to 30:  
'subtask003_mctaco_question_generation_event_duration'  
'subtask034_winogrande_question_modification_object'  
'subtask040_qasc_question_generation'  
'subtask045_miscellaneous_sentence_paraphrasing'  

## Library Installation:
```
python install_dependencies.py

pip install openai
pip install transformers
```

## Generate Predictions
Generate predictions for baseline or reframed instructions:

```
python {baseline/reframed}.py --model_name={model_name} --number_of_instances=50 --number_of_examples 5 --API_TOKEN={API_TOKEN}
```

We use 50 instances for each task and provided 5 examples in each prompt. For all versions of gpt2, we limit the examples for the following tasks due to input token limit:

We set it to 0 for:
subtask002_quoref_answer_generation

We set it to 2 for:
subtask052_multirc_identify_bad_question

model_name is one of the following:

1) gpt2
2) gpt2-xl
3) gpt2-large
4) gpt3_davinci (for gpt3)
5) gpt3 (for gpt3 instruct)

API_token is needed only in case of gpt3_davinci or gpt3

## Output Files:

The generated predictions are stored in folder named output_files or output_files_reframed for baseline and reframed experiments respectively.

The folder will have sub folders for each model used. 

For each task, a prediction file will be generated with the following nomenclature:

{output_files/output_files_reframed}/{model_name}/{task_name}_prediction.json


## Evaluation:

Some tasks have multiple correct outputs. To facilitate evaluation, each ground truth value for an instance is compared against the generated output.
```
python evaluate_multi.py --dataset_file {prediction file}
```

where the prediction file follows the nomenclature described above.

The ground truth value having the best result is used and stored in another file with the following nomenclature:

{output_files/output_files_reframed}/{model_name}/{task_name}_prediction_final.json

## Results:

![alt text](image/result.png)




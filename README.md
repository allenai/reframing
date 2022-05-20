# Reframing Instructional Prompts to GPTk's Language

## Description
This repository contains the code of the paper [Reframing Instructional Prompts to GPTk's Language](https://arxiv.org/pdf/2109.07830.pdf). We use 12 tasks that belongs to the evaluation split of [NATURAL INSTRUCTIONS v1.1](https://instructions.apps.allenai.org/). 

There are two sets of results. The first set (baseline) is obtained using raw instructions of these tasks. The second set (reframed) is obtained using the reframed instructions. Techniques to reframe instructions are described in [paper](https://arxiv.org/pdf/2109.07830.pdf). 

## Raw instructions

Each prompt for raw instructions is defined using the "Definition", "Emphasis & Caution", "Things to Avoid", "Prompt", "Positive Examples Full Only" fields, in that order, from files in Dataset_Jsons.

The script named ```src/encoding/encodeinstructions``` outputs the encoded raw instructions.

## Reframed instructions:

Reframed instructions for all tasks are present inside the ```reframed_instructions``` directory.

The script in ```src/encoding/encodeinstructions_reframed```  outputs the encoded reframed instructions. 

## Library Installation:
```
python src/installation/install_dependencies.py

pip install openai
pip install transformers
```

## Generate Predictions
Generate predictions for baseline or reframed instructions:

```
python src/generation/{baseline/reframed}.py --model_name={model_name} --number_of_instances=50 --number_of_examples 5 --API_TOKEN={API_TOKEN}
```

model_name is one of the following:

1) gpt2
2) gpt2-xl
3) gpt2-large
4) gpt3_davinci (for gpt3)
5) gpt3 (for gpt3 instruct)

API_token is needed only in case of gpt3_davinci or gpt3

## Output Files:

Sample generated predictions with reframing are stored in ```output_files_reframed```.

The folder has sub folders for each model used. 

For each task, a prediction file has the following nomenclature:

{output_files_reframed}/{model_name}/{task_name}_prediction.json


## Evaluation:

```python src/evaluate/evaluate.py --dataset_file {prediction file}```

## How to cite
Feel free to cite us: 
```bibtex
@article{mishra2021reframing,
  title={Reframing Instructional Prompts to GPTk's Language},
  author={Mishra, Swaroop and Khashabi, Daniel and Baral, Chitta and Choi, Yejin and Hajishirzi, Hannaneh},
  journal={ACL Findings},
  year={2021}
}
```



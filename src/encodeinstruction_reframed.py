import json
import os
import random
import math
def encodeinstruction(task, model_name, instruction_structure =['Positive Examples Full Only'], number_of_examples=0, number_of_instances= 100):
    list_task = [
        {
            "task": 'subtask002_quoref_answer_generation', 
            "prompt": "Answer the following Question based on the passage. Your answer must be a single phrase in the passage. You need to identify mutliple references to the same entity such as person, place etc. while answering.\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": ""
        },
        {
            "task": 'subtask003_mctaco_question_generation_event_duration', 
            "prompt": "Use 'how long' in your question based on the input sentence.\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": ""
        },
        {
            "task": 'subtask005_mctaco_wrong_answer_generation_event_duration', 
            "prompt": "Write a wrong answer to the question asked. Use 'hours, minutes, seconds, years, days, months or weeks' in your answer to the question based on the given sentence.\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": " Generate an answer in 2 words"
        },
        {
            "task": 'subtask008_mctaco_wrong_answer_generation_transient_stationary', 
            "prompt": "Write a wrong answer to the given question\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": ""
        },
        {
            "task": 'subtask022_cosmosqa_passage_inappropriate_binary', 
            "prompt": "Read the given context and if the the context is inappropriate (e.g., pornographic) or nonsensical (e.g., cannot determine what happenings the context is about), indicate via \"yes\". Otherwise, response via \"no\".\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": ""
        },
        {
            "task": 'subtask033_winogrande_answer_generation', 
            "prompt": "Fill in the blank. The answer is one of the objects present in the question.\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": ""
        },
        {
            "task": 'subtask034_winogrande_question_modification_object', 
            "prompt": "Do minor change to the given question such that its answer changes to another object in the question\n\n{0}\n\n{1}\nQuestion:",
            "string_to_append": ""
        },
        {
            "task": 'subtask039_qasc_find_overlapping_words', 
            "prompt": "Generate an overlapping word between the given two sentences. When you find the overlapping words, they don't have to match exactly, e.g., \"survival\" and \"survive\" are valid overlapping words.\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": " Generate one word common to given sentences"
        },
        {
            "task": 'subtask040_qasc_question_generation', 
            "prompt": "Turn the given fact into a question by a simple rearrangement of words. This typically involves replacing some part of the given fact by a WH word. For example, replacing subject of the provided fact with the word \"what\" can form a valid question.\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": ""
        },
        {
            "task": 'subtask044_essential_terms_identifying_essential_words', 
            "prompt": "Generate words or phrases of the question that are essential for choosing the correct answer.\n\n{0}\n\n{1}\nEssential words:",
            "string_to_append": " Generate essential words of the given question separated by comma"
        },
        {
            "task": 'subtask045_miscellaneous_sentence_paraphrasing', 
            "prompt": "Generate a paraphrase of the given sentence in the input.\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": ""
        },
        {
            "task": 'subtask052_multirc_identify_bad_question', 
            "prompt": "You are given a passage and a question. Generate \"yes\" if the question is a bad question (grammatical errors, typing mistakes, etc. or might not make sense in the context of the paragraph (for instance, it might not be related to the content of the paragraph or not be answerable at all)), generate \"no\" otherwise.\n\n{0}\n\n{1}\nAnswer:",
            "string_to_append": " Generate \"Yes\" if the question is bad, else generate \"No\""
        }
    ]
    
    with open('Dataset_Jsons/'+task+'.json') as json_file:
        data = json.load(json_file)

    indexlist=list(range(60,len(data['Instances'])-1, math.floor((len(data['Instances'])-60)/number_of_instances)))[:number_of_instances]
    
    task_item = [i["prompt"] for i in list_task if i["task"] == task][0]
    string_to_append = [i["string_to_append"] for i in list_task if i["task"] == task][0]
    examples = ""
    
    min_examples = min(number_of_examples, len(data["Examples"]["Positive Examples"]))
    examples = ""
    for p_example in data["Examples"]["Positive Examples"][:min_examples]:
        if task == "subtask034_winogrande_question_modification_object":
            examples = examples + p_example["input"] + string_to_append + "\nQuestion: " + p_example["output"] + "\n\n"
        elif task == "subtask044_essential_terms_identifying_essential_words":
            examples = examples + p_example["input"] + string_to_append + "\nEssential Words: " + p_example["output"] + "\n\n"
        else:
            examples = examples + p_example["input"] + string_to_append + "\nAnswer: " + p_example["output"] + "\n\n"
    
    examples = examples.strip()
    
    instruction_list = []
    true_answers = []
    true_answers_new = []
    for inst in indexlist:
        instruction_list.append(task_item.format(examples, data["Instances"][inst]["input"] + string_to_append))
        true_answers.append(data["Instances"][inst]["output"])
        true_answers_new.append(' '.join(data["Instances"][inst]["output"]))
    task_answers = []
    with open('output_files_reframed/' + model_name + "/" +task+'_prediction.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps({"true": true_answers, "prediction": task_answers}, ensure_ascii=False, indent = 4))
        
    with open('output_files_reframed/' + model_name + "/" +task+'_prediction_new.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps({"true": true_answers_new, "prediction": task_answers}, ensure_ascii=False, indent = 4))
    
    return instruction_list
    



import json
import os
import random
import math
def encodeinstruction(task, model_name, instruction_structure =['Positive Examples Full Only'], number_of_examples=0, number_of_instances= 100):
    
    with open("utils/instruction_templates/" + task + ".txt", "r") as f:
        lines = f.readlines()
    

    with open('Dataset_Jsons/'+task+'.json') as json_file:
        data = json.load(json_file)

    indexlist=list(range(60,len(data['Instances'])-1, math.floor((len(data['Instances'])-60)/number_of_instances)))[:number_of_instances]
    
    task_item = str(lines[0]).replace(r'\n', '\n')
    string_to_append = str(lines[1]).replace(r'\n', '\n') if len(lines) == 2 else ""
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
    for inst in indexlist:
        instruction_list.append(task_item.format(examples, data["Instances"][inst]["input"] + string_to_append))
        true_answers.append(data["Instances"][inst]["output"])
        

    task_answers = []

    
    with open('output_files_reframed/' + model_name + "/" +task+'_prediction.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps({"true": true_answers, "prediction": task_answers}, ensure_ascii=False, indent = 4))
        
    
    return instruction_list
    



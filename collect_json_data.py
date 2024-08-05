

# This script finds all the files ending with jsonl and merge them into one dataset 
import os
from datasets import load_dataset, DatasetDict, Dataset
import json

# The folders to load data
all_folder_path = [
        '/home/cyeab/tora/RLHF4MATH_Dev/inference/math_middle_collect/deepseek_rl/math',
]

output_dir = ""

def get_samples(one_line):
    idx = one_line['idx']
    gt = one_line['gt']
    level = one_line['level']
    p_type = one_line['type']
    all_solutions = one_line['my_solu']
    all_preds = one_line['pred']
    tmp_list = []
    for j in range(len(all_solutions)):
        tmp_list.append(
            {
                "idx": idx,
                "gt": gt,
                "level": level,
                "type": p_type,
                "my_solu": all_solutions[j],
                "pred": all_preds[j]
            }
        )
    return tmp_list
    
all_data = []
for folder_path in all_folder_path:
    jsonl_files = [folder_path + '/' + f for f in os.listdir(folder_path) if f.endswith('.jsonl')]
    for dir_ in jsonl_files:
        with open(dir_, 'r') as file:
            for line in file:
                all_data.extend(get_samples(json.loads(line)))


print(all_data[0])
print(all_data[1])
print(all_data[1]['my_solu'] == all_data[0]['my_solu'])

print(len(all_data))
    #for dir_ in jsonl_files:
        #ds_test = load_dataset('json', data_files=dir_, split='train')
        #for sample in ds_test:
        #    all_data.append(sample)

dict_data = {
    "idx": [d['idx'] for d in all_data],
    "gt": [d['gt'] for d in all_data],
    "level": [d['level'] for d in all_data],
    "type": [d['type'] for d in all_data],
        "my_solu": [d['my_solu'] for d in all_data],
    "pred": [d['pred'] for d in all_data],
}

dataset = Dataset.from_dict(dict_data)
DatasetDict({'train': dataset}).push_to_hub(output_dir)

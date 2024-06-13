import os
from datasets import load_dataset

# 设置你的文件夹路径
all_folder_path = ['/home/wexiong_google_com/wx/ToRA_math/src/output1/llm-agents/tora-code-34b-v1.0/math',
        '/home/wexiong_google_com/wx/ToRA/src/output1/llm-agents/tora-code-34b-v1.0/math']
output_dir='all_math.json'


#jsonl_files = [folder_path + '/' + f for f in os.listdir(folder_path) if f.endswith('.jsonl')]
#print(jsonl_files)

all_data = []
for folder_path in all_folder_path:
    jsonl_files = [folder_path + '/' + f for f in os.listdir(folder_path) if f.endswith('.jsonl')]
    for dir_ in jsonl_files:
        ds_test = load_dataset('json', data_files=dir_, split='train')
        for sample in ds_test:
            all_data.append(sample)


import json

output_eval_dataset = {}
output_eval_dataset["type"] = "text_only"
output_eval_dataset["instances"] = all_data
print("I collect ", len(all_data), "samples")


with open(output_dir, "w", encoding="utf8") as f:
    json.dump(output_eval_dataset, f, ensure_ascii=False)

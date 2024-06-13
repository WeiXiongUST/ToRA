import os
from datasets import load_dataset

# 设置你的文件夹路径
folder_path = 'xx'
output_dir=''
# 获取所有.jsonl文件
jsonl_files = [f for f in os.listdir(folder_path) if f.endswith('.jsonl')]

all_data = []
for dir in jsonl_files:
  ds_test = load_dataset('json', data_files=dir, split='train')
  for sample in ds_test:
    all_data.append(sample)


import json

output_eval_dataset = {}
output_eval_dataset["type"] = "text_only"
output_eval_dataset["instances"] = all_data
print("I collect ", len(gathered_data), "samples")


with open(output_dir, "w", encoding="utf8") as f:
    json.dump(output_eval_dataset, f, ensure_ascii=False)

from datasets import load_dataset
import re
dataset_dir = ""

output_dir = ""

ds = load_dataset('json', data_files=dataset_dir, split='train', field='instances')

def filter_example(example):
    try: 
        if abs(float(example['pred'][0]) - float(example['gt'])) < 0.01:
            return True
    except:
        if example['pred'][0] == example['gt']:
            return True
    else:
        return False

ds_filtered = ds.filter(filter_example, num_proc=32)


def parse_conversation(text):
    # Split the text based on "user\n" and "assistant\n" to identify turns
    splitters = r'<\|user\|>\n|<\|assistant\|>\n'  # 使用 '|' 来表示'或'，匹配'user'或'assistant'
    entries = [z for z in re.split(splitters, text) if z]

    #entries = text.strip().split('<|user|>\n').split('<|assistant|>\n')
    if len(entries) % 2 != 0:
        #print(entries)
        print('not user-assistant-user-assistant')
        return []
    structured_conversation = []
    #last_role = -1
    # 0 for user, 1 for assitant
    role = 'user'
    to_comp = ''
    for entry in entries:
        # Check if it's a new role identifier and update the role
        if role == 'user':
            structured_conversation.append({"role": role, "content": entry})
            role = "assistant"
            to_comp += '<|user|>\n' + entry
        elif role == "assistant":
            structured_conversation.append({"role": role, "content": entry})
            role = "user"
            to_comp += '<|assistant|>\n' + entry
    if to_comp != text:
        #print(to_comp)
        #print(text)
        print("to_comp != text")
        return []
    
    count = text.count('\\boxed')
    if count != 1:
        print("no boxed or too many boxed")
        return []

    return structured_conversation

new_data = []
for sample in ds_filtered:
    a = parse_conversation(ds_filtered[0]['my_solu'][0])
    new_data.append(a)

import json

output_eval_dataset = {}
output_eval_dataset["type"] = "text_only"
output_eval_dataset["instances"] = new_data
print("I collect ", len(gathered_data), "samples")


with open(output_dir, "w", encoding="utf8") as f:
    json.dump(output_eval_dataset, f, ensure_ascii=False)

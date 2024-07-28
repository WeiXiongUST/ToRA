
from dataclasses import dataclass, field
from typing import Optional
import argparse
import peft
import torch
from peft import PeftConfig, PeftModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer, HfArgumentParser

parser = argparse.ArgumentParser(description='Merge base model and LoRA using Peft')
parser.add_argument('--base_model', type=str, 
                    default='/home/xingshuo/Reward-Model/gemma-2-9b-it')
parser.add_argument('--lora', type=str, 
                    default='/home/xingshuo/preference_prediction/output/gemma9b_classifier3_lora256_lr1e-4_maxlen4096_train0.8_extend_arena_filtered_augtrain/logs/checkpoint-1912')
parser.add_argument('--output', type=str,
                    default='gemma9b_classifier3_lora256_lr1e-4_maxlen4096_train0.8_extend_arena_filtered_augtrain_merged_models')
args = parser.parse_args()

peft_config = PeftConfig.from_pretrained(args.lora)
model = AutoModelForSequenceClassification.from_pretrained(
    peft_config.base_model_name_or_path,
    return_dict=True,
    torch_dtype=torch.float16,
    num_labels=3
)
tokenizer = AutoTokenizer.from_pretrained(peft_config.base_model_name_or_path)

# Load the LoRA model
model = PeftModel.from_pretrained(model, args.lora)
model = model.merge_and_unload()

print(model)

model.save_pretrained(args.output)

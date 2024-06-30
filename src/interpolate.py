import torch
#!/usr/bin/env python
# coding=utf-8
# Copyright 2023 Statistics and Machine Learning Research Group at HKUST. All rights reserved.
"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
import json
import os
import sys
from transformers import HfArgumentParser, AutoModelForCausalLM


new_dir = "/home/cyeab/axtool/models/llama8b_it_data_henrydong/checkpoint-1308"
base_dir = "meta-llama/Meta-Llama-3-8B-Instruct"
weight_ensamble_save_path = "/home/cyeab/axtool/models/llama8b_it_data_henrydong/weighted_merge/weight_07"
weight_ensamble_ratios = [0.7]

# Get the paths and ratios of weight-ensamble models.
weight_ensamble_names_paths = [new_dir, base_dir]
weight_ensamble_ratios.append(1 - weight_ensamble_ratios[0])
assert len(weight_ensamble_ratios) == 2, 'Only 2 merge is supported.'
print('Model Paths:', weight_ensamble_names_paths)
print('Model Ratio:', weight_ensamble_ratios)



base_model = None
backend_models = []
for model_path in weight_ensamble_names_paths:
    #model_args.model_name_or_path = model_path
    print('loading:', model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)#, torch_dtype=torch.bfloat16)
    backend_models.append(model.to('cpu'))
    if base_model is None:
        base_model = model
    print('Finish load:', model_path)
base_backend_model = backend_models[0]
print('Finish load All:', base_backend_model)
# print('Base State dicts', base_backend_model.state_dict())

updated_state_dict = {}
for key in base_backend_model.state_dict():
    ensambled_state_dicts = [ratio * backend_model.state_dict()[key] for backend_model, ratio in zip(backend_models, weight_ensamble_ratios)]
    # print(ensambled_state_dicts)
    updated_state_dict[key] = sum(ensambled_state_dicts)
    # print(updated_state_dict.size())
print('WiSE State dicts', base_backend_model.state_dict())
base_backend_model.load_state_dict(updated_state_dict)
print(weight_ensamble_save_path)
base_model.save_pretrained(weight_ensamble_save_path)

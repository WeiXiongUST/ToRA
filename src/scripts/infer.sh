set -ex

MODEL_NAME_OR_PATH="llm-agents/tora-code-34b-v1.0"
#"llm-agents/tora-code-34b-v1.0"
#"llm-agents/tora-code-34b-v1.0"
# MODEL_NAME_OR_PATH="llm-agents/tora-70b-v1.0"

# DATA_LIST = ['math', 'gsm8k', 'gsm-hard', 'svamp', 'tabmwp', 'asdiv', 'mawps']

DATA_NAME="math"
# DATA_NAME="gsm8k"
OUTPUT_DIR="./output1"

SPLIT="train"
PROMPT_TYPE="tora"
NUM_TEST_SAMPLE=-1

#--use_train_prompt_format \

CUDA_VISIBLE_DEVICES=0 TOKENIZERS_PARALLELISM=false \
python -um infer.inference \
--model_name_or_path ${MODEL_NAME_OR_PATH} \
--data_name ${DATA_NAME} \
--output_dir ${OUTPUT_DIR} \
--split ${SPLIT} \
--prompt_type ${PROMPT_TYPE} \
--num_test_sample ${NUM_TEST_SAMPLE} \
--seed 0 \
--temperature 1.0 \
--n_sampling 1 \
--top_p 1 \
--start 0 \
--end -1 \

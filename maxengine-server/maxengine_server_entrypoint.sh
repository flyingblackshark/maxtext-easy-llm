#!/bin/bash
cd /maxtext
python3 -m MaxText.maxengine_server \
MaxText/configs/base.yml \
--model_name=gemma3-27b \
--tokenizer_path=assets/tokenizer.gemma3 \
--per_device_batch_size=4 \
--max_prefill_predict_length=8192 \
--max_target_length=16384 \
--attention=flash \
--attention_type=global \
--async_checkpointing=false \
--ici_fsdp_parallelism=1 \
--ici_autoregressive_parallelism=-1 \
--ici_tensor_parallelism=1 \
--scan_layers=false \
--weight_dtype=bfloat16 \
--load_parameters_path=gs://fbs-usc1/unscanned_chkpt_233/checkpoints/0/items
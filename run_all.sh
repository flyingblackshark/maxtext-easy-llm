sudo docker run --name maxengine-server \
  --net=host \
  maxengine-server:dev \
  --model_name=gemma3-27b \
  --tokenizer_path=assets/tokenizer.gemma3 \
  --per_device_batch_size=4 \
  --max_prefill_predict_length=1024 \
  --max_target_length=2048 \
  --async_checkpointing=false \
  --ici_fsdp_parallelism=1 \
  --ici_autoregressive_parallelism=-1 \
  --ici_tensor_parallelism=1 \
  --scan_layers=false \
  --weight_dtype=bfloat16 \
  --load_parameters_path=gs://fbs-usc1/unscanned_chkpt_233/checkpoints/0/items
sudo docker run -d --name jetstream-http --net=host \
jetstream-http:dev

sudo docker run -d --name gradio \
--net=host \
-e CONTEXT_PATH="/generate" \
-e HOST="http://127.0.0.1:8000" \
-e LLM_ENGINE="max" \
-e MODEL_ID="gemma" \
-e USER_PROMPT="<start_of_turn>user\nprompt<end_of_turn>\n" \
-e SYSTEM_PROMPT="<start_of_turn>model\nprompt<end_of_turn>\n" \
jetstream-gradio:dev
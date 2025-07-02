# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import gradio as gr
import os
import json

disable_system_message = False
if "DISABLE_SYSTEM_MESSAGE" in os.environ:
    disable_system_message = os.environ["DISABLE_SYSTEM_MESSAGE"]


def inference_interface(message, history, model_temperature, top_p, max_tokens):

    json_message = {}
    json_message.update({"temperature": model_temperature})
    json_message.update({"top_p": top_p})
    json_message.update({"max_tokens": max_tokens})
    json_message.update({"stream": True})  # Enable streaming
    final_message = process_message(message, history)
    json_message.update({"prompt": final_message})
    
    # Use streaming response
    for chunk in post_request_stream(json_message):
        yield chunk


def process_message(message, history):
    user_prompt_format = ""
    system_prompt_format = ""

    # if env prompts are set, use those
    if "USER_PROMPT" in os.environ:
        user_prompt_format = os.environ["USER_PROMPT"]

    if "SYSTEM_PROMPT" in os.environ:
        system_prompt_format = os.environ["SYSTEM_PROMPT"]

    print("* History: " + str(history))

    user_message = ""
    system_message = ""
    history_message = ""

    if len(history) > 0:
        # we have history
        for item in history:
            user_message = user_prompt_format.replace("prompt", item[0])
            system_message = system_prompt_format.replace("prompt", item[1])
            history_message = history_message + user_message + system_message

    new_user_message = user_prompt_format.replace("prompt", message)

    # append the history with the new message and close with the turn
    aggregated_message = history_message + new_user_message
    return aggregated_message


def post_request(json_message):
    print("*** Request" + str(json_message), flush=True)
    response = requests.post(
        os.environ["HOST"] + os.environ["CONTEXT_PATH"], json=json_message
    )
    json_data = response.json()
    print("*** Output: " + str(json_data), flush=True)
    return json_data


def post_request_stream(json_message):
    """Handle streaming response from the server."""
    print("*** Streaming Request" + str(json_message), flush=True)
    
    response = requests.post(
        os.environ["HOST"] + os.environ["CONTEXT_PATH"], 
        json=json_message,
        stream=True
    )
    
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}: {response.text}")
    
    accumulated_text = ""
    buffer = ""
    
    # Process streaming response chunk by chunk
    for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
        if chunk:
            buffer += chunk
            
            # Try to extract complete JSON objects from buffer
            while True:
                try:
                    # Find the end of a JSON object
                    decoder = json.JSONDecoder()
                    obj, idx = decoder.raw_decode(buffer)
                    
                    # Successfully parsed a JSON object
                    if "text" in obj:
                        chunk_text = obj["text"]
                        accumulated_text += chunk_text
                        print(f"*** Stream chunk: {chunk_text}", flush=True)
                        yield accumulated_text
                        
                        # Check for end of turn marker
                        # if "<end_of_turn>" in chunk_text:
                        #     print("*** Detected <end_of_turn>, stopping stream", flush=True)
                        #     return
                    
                    # Remove the parsed JSON from buffer
                    buffer = buffer[idx:].lstrip()
                    
                except json.JSONDecodeError:
                    # No complete JSON object in buffer yet, wait for more data
                    break
    
    print(f"*** Final accumulated text: {accumulated_text}", flush=True)


with gr.Blocks(fill_height=True) as app:
    html_text = "You are chatting with: gemma3"
    gr.HTML(value=html_text)

    model_temperature = gr.Slider(
        minimum=0.1, maximum=1.0, value=0.9, label="Temperature", render=False
    )
    top_p = gr.Slider(minimum=0.1, maximum=1.0, value=0.95, label="Top_p", render=False)
    max_tokens = gr.Slider(
        minimum=1, maximum=4096, value=256, label="Max Tokens", render=False
    )

    gr.ChatInterface(
        inference_interface, additional_inputs=[model_temperature, top_p, max_tokens]
    )

app.launch(server_name="0.0.0.0")
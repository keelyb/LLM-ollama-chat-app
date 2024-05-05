try:
    import requests
    import json
    import gradio as gr
    import time
except:
    print("Please install the required libraries: requests, json, gradio, time. See README")
    exit
try:
  import platform
  import psutil
except ImportError:
  pass

url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json',
}

conversation_history = []


def generate_response(model, prompt):

    start = time.time()

    # print("Gradio version:" + gr.__version__)
    conversation_history.append(prompt)

    full_prompt = "\n".join(conversation_history)
    # print("conversation history: " + full_prompt)
    

    data = {
        # "model": "mistral",
        "model": f"""{model}""",
        "stream": False,
        "prompt": full_prompt,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    end = time.time()
    elapsed_time = round(end - start,3)
    # print(f"Function took {elapsed_time} seconds to run")

    try:
        print(f"System: {platform.system()} ") 
        print(f"Machine: {platform.machine()}")
        print(f"Memory: {psutil.virtual_memory().total / (1024**3)} GB") 
    except ImportError:
        pass

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response + "\n\n" + f"Model: {model} processing took {elapsed_time} seconds to run"
    else:
        print("Error:", response.status_code, response.text)
        return None
    
 
    



iface = gr.Interface(    
    fn=generate_response,
    inputs=[
        gr.Dropdown(
            ["tinyllama","superman"], label="Model", info="Select a model:"),
        gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
        ],
    outputs="text"
)

iface.launch()

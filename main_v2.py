import requests
import json
import gradio as gr
from pydantic import BaseModel, Field

# --------------------------------------
# 1. Define a Pydantic model for the LLM request.
# --------------------------------------
class GenerateRequest(BaseModel):
    model: str = Field(..., description="The local model name, e.g., llama2 or gemma3.")
    stream: bool = Field(False, description="Whether to stream the output.")
    prompt: str = Field(..., description="The entire conversation history (or last chunk).")

# --------------------------------------
# 2. Load the CV text. 
#    (Assuming your 20-page CV is in 'cv.txt'.)
#    If you have it in a string, just store it directly.
# --------------------------------------
cv_text = ""
try:
    with open("cv.txt", "r", encoding="utf-8") as f:
        cv_text = f.read()
except FileNotFoundError:
    cv_text = "Curriculum Vitae goes here if 'cv.txt' is not found."

# --------------------------------------
# 3. Create conversation_history with the CV as initial context
# --------------------------------------
conversation_history = [cv_text]

# The endpoint you’re calling
url = "http://localhost:11434/api/generate"

# Headers for requests
headers = {
    'Content-Type': 'application/json',
}

def generate_response(model, prompt):
    print("Gradio version:", gr.__version__)

    # Append user prompt to the conversation
    conversation_history.append(prompt)

    # Build the full_prompt from the conversation so far
    full_prompt = "\n".join(conversation_history)

    # Construct our pydantic request object
    req_obj = GenerateRequest(
        model=model,
        stream=False,
        prompt=full_prompt
    )

    # Convert it to JSON
    data_str = req_obj.json()

    # Make the POST call to your local LLM endpoint
    response = requests.post(url, headers=headers, data=data_str)

    if response.status_code == 200:
        response_json = response.json()
        actual_response = response_json.get("response", "")
        conversation_history.append(actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return f"Error: {response.status_code} - {response.text}"

# --------------------------------------
# 4. Gradio interface
# --------------------------------------
iface = gr.Interface(
    fn=generate_response,
    inputs=[
        gr.Dropdown(
            ["llama2", "tinyllama", "deepseek-r1", "midiman",
             "dnaman", "dnaman_deepseek_r1", "gemma3"],
            label="Model",
            info="Select one of your locally installed models"
        ),
        gr.Textbox(lines=2, placeholder="Enter your prompt here...")
    ],
    outputs="text"
)

iface.launch()

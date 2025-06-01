from llama_cpp import Llama
import os

MODEL_PATH = os.getenv("MODEL_PATH", r"C:\llm_models\lm_studio\mistral-7b-instruct-v0.1.Q5_0.gguf")

llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=8, n_gpu_layers=40, verbose=False)

instruction = (
    "You are a helpful and polite customer support assistant. "
    "Avoid vague or overly generic responses. Always be clear and actionable."
)

def generate_response(prompt: str) -> str:
    full_prompt = f"[INST] {instruction} {prompt} [/INST]"
    response = llm(full_prompt, max_tokens=512, temperature=0.7, stop=["</s>"])
    return response['choices'][0]['text'].strip()

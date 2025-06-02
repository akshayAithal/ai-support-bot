from llama_cpp import Llama
import os

GGUF_DIR = "models" #"models/latest_gguf"
default_model_path = next((f"{GGUF_DIR}/{f}" for f in os.listdir(GGUF_DIR) if f.endswith(".gguf")), None)

MODEL_PATH = os.getenv("MODEL_PATH", default_model_path)


llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=8, n_gpu_layers=40, verbose=False)

instruction = (
    "You are a helpful and polite customer support assistant. "
    "Avoid vague or overly generic responses. Always be clear and actionable."
)

def generate_response(prompt: str) -> str:
    full_prompt = f"[INST] {instruction} {prompt} [/INST]"
    response = llm(full_prompt, max_tokens=512, temperature=0.7, stop=["</s>"])
    return response['choices'][0]['text'].strip()

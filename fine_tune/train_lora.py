from datasets import load_dataset
from peft import get_peft_model, LoraConfig, TaskType, PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch

import os

def get_next_model_version(base_dir="models"):
    versions = [
        int(name.split("_v")[-1])
        for name in os.listdir(base_dir)
        if name.startswith("TinyLlama-finetuned_v")
    ]
    next_version = max(versions, default=0) + 1
    return f"TinyLlama-finetuned_v{next_version}"


# Load base model + tokenizer
model_path = os.getenv("MODEL_FILES", r"models\TinyLlama-1.1B-Chat-v1.0")
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load dataset
dataset = load_dataset("json", data_files="fine_tune/low_rated_feedback.jsonl")

def tokenize(sample):
    conversation = sample["conversation"]

    encoded = tokenizer(
        conversation,
        truncation=True,
        padding="max_length",
        max_length=512
    )

    labels = encoded["input_ids"].copy()

    # Mask tokens not related to "AI:" response
    ai_start = conversation.find("AI:")
    if ai_start != -1:
        ai_tokens = tokenizer(conversation[ai_start:], truncation=True, padding="max_length", max_length=512)["input_ids"]
        # Replace all non-AI tokens with -100
        for i in range(len(labels)):
            if i < len(labels) - len(ai_tokens):
                labels[i] = -100

    encoded["labels"] = labels
    return encoded

tokenized = dataset.map(tokenize)

# LoRA Config
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    bias="none",
    target_modules=["q_proj", "v_proj"]
)

model = get_peft_model(model, peft_config)

# Training Args
training_args = TrainingArguments(
    output_dir="lora_out",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=2,
    save_strategy="epoch",
    logging_dir="./logs",
    bf16=True,
    report_to="none"
)

trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=tokenized["train"]
)

trainer.train()
trainer.save_model("lora_out") 

# ✅ Final Step: Merge LoRA into base model
print("🔁 Merging LoRA weights into base model...")
merged_model = PeftModel.from_pretrained(
    AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.bfloat16),
    "lora_out",
    local_files_only=True
)
merged_model = merged_model.merge_and_unload()

# Save merged model
save_dir = f"models\\{get_next_model_version()}"
merged_model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"✅ Merged model saved to: {save_dir}")
import subprocess
subprocess.run([
    "python3", convert_script,
    "--outtype", "gguf",
    "--outfile", gguf_path,
    save_dir  # directory with safetensors or .bin
])

latest_symlink = "models/latest_gguf"
if os.path.islink(latest_symlink) or os.path.exists(latest_symlink):
    os.remove(latest_symlink)
os.symlink(save_dir, latest_symlink)

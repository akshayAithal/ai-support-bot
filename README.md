
# 🧠 AI-Powered Customer Support System

A full-stack AI chatbot system that offers 24/7 customer support with automated feedback collection, learning from negative ratings, fine-tuning LLMs, and a CI/CD-ready architecture using Flask, SQLite, Docker, and LoRA-based retraining.

---

## 🚀 Features

- ✅ Conversational LLM chatbot using Mistral-7B-Instruct (GGUF + llama-cpp-python)
- ✅ Web UI built with Flask + Jinja2 (no JS framework)
- ✅ Chat session persistence using SQLite + SQLAlchemy
- ✅ User feedback collection (rating)
- ✅ Weekly feedback export and model fine-tuning with LoRA
- ✅ Automatic versioning: `mistral-finetuned_vX`
- ✅ Dockerized with `docker-compose`
- ✅ CI/CD-ready training loop with cron or GitHub Actions

---

## 🗂 Project Structure

```
customer_bot/
├── app.py                    # Flask app with chat + feedback logic
├── model_runner.py           # LLM model loading (llama-cpp-python)
├── models.py                 # SQLAlchemy models for chat & feedback
├── export_feedback.py        # Extracts low-rated chat data
├── fine_tune/
│   └── train_lora.py         # Fine-tuning script using LoRA
├── templates/
│   └── index.html            # Jinja2 UI template
├── static/
│   └── style.css             # Basic styling
├── models/
│   ├── mistral-fp16/         # Base HF model for fine-tuning
│   ├── mistral-finetuned_v1/ # Fine-tuned model (merged)
│   └── .keep                 # Keeps folder structure in Git
├── requirements.txt          # Python dependencies
├── Dockerfile                # App + training Docker image
├── docker-compose.yaml       # Compose setup for web + cron jobs
├── .gitignore
└── README.md
```

---

## 💬 Local Usage

### 1. Clone the project
```bash
git clone https://github.com/yourusername/ai-support-bot.git
cd ai-support-bot
```

### 2. Download model manually (GGUF format)
- Download from: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF
- Place `.gguf` model under `./models/`

### 3. Run the chatbot
```bash
docker-compose up --build
```

Visit [http://localhost:5000](http://localhost:5000)

---

## 🔁 Weekly Auto-Retrain Workflow

- `export_feedback.py` extracts chats with ratings ≤2
- `train_lora.py` fine-tunes on them using LoRA
- Merged model is saved as `models/mistral-finetuned_vX/`
- Can be converted to GGUF for inference deployment

---

## 🔧 CI/CD Friendly

Integrate with GitHub Actions, Jenkins, or GitLab CI:

```yaml
steps:
  - run: python export_feedback.py
  - run: python fine_tune/train_lora.py
  - run: docker build -t yourregistry/ai-support-bot:vX .
  - run: docker push yourregistry/ai-support-bot:vX
```

---

## 🧑‍💻 Credits

Built by Akshay Aithal using:
- Flask
- llama-cpp-python
- PEFT + LoRA

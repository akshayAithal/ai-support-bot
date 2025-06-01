# 🧠 AI-Powered Customer Support System

A full-stack AI chatbot system that offers 24/7 customer support with automated feedback collection, learning from negative ratings, fine-tuning LLMs, and a full CI/CD-ready architecture using Flask, SQLite, Docker, and LoRA-based model retraining.

---

## 🚀 Features

- ✅ Conversational LLM chatbot using `mistral-7B-instruct` (GGUF + llama-cpp-python)
- ✅ Web UI built with Flask + Jinja2 (no JS framework)
- ✅ Chat session persistence using SQLite + SQLAlchemy
- ✅ User feedback collection (rating + comment)
- ✅ Weekly feedback export and model fine-tuning with LoRA
- ✅ Automatic versioning: `mistral-finetuned_vX`
- ✅ Dockerized with `docker-compose`
- ✅ CI/CD-ready training loop with cron or GitHub Actions

---

## 🗂 Project Structure
customer_bot/
├── app.py # Flask app with chat + feedback logic
├── model_runner.py # LLM model loading (llama-cpp-python)
├── models.py # SQLAlchemy models for chat & feedback
├── export_feedback.py # Extracts low-rated chat data
├── fine_tune/
│ └── train_lora.py # Fine-tuning script using LoRA
├── templates/
│ └── index.html # Jinja2 UI template
├── static/
│ └── style.css # Basic styling
├── models/
│ ├── mistral-fp16/ # Base HF model for fine-tuning
│ ├── mistral-finetuned_v1/ # Fine-tuned model (merged)
│ └── .keep # Keeps folder structure in Git
├── requirements.txt # Python dependencies
├── Dockerfile # App + training Docker image
├── docker-compose.yaml # Compose setup for web + cron jobs
├── .gitignore
└── README.md

Copy
Edit


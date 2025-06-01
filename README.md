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


from models import db, Feedback, ChatMessage
from flask import Flask
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def export_low_rated_feedback(filename="low_rated_feedback.jsonl"):
    with app.app_context():
        data = []
        feedbacks = Feedback.query.filter(Feedback.rating <= 2).all()
        for fb in feedbacks:
            ai_msg = ChatMessage.query.get(fb.message_id)
            if not ai_msg:
                continue

            # Get all messages before the AI response in this session
            chat_history = ChatMessage.query.filter(
                ChatMessage.session_id == fb.session_id,
                ChatMessage.timestamp <= ai_msg.timestamp
            ).order_by(ChatMessage.timestamp).all()

            history_text = ""
            for msg in chat_history:
                speaker = "User" if msg.role == "user" else "AI"
                history_text += f"{speaker}: {msg.text}\n"

            data.append({
                "conversation": history_text.strip(),
                "rating": fb.rating,
                "comment": fb.comment
            })

        with open(filename, "w", encoding="utf-8") as f:
            for entry in data:
                f.write(json.dumps(entry) + "\n")

        print(f"Exported {len(data)} entries to {filename}")

if __name__ == "__main__":
    export_low_rated_feedback()

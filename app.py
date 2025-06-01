from flask import Flask, request, render_template, redirect, url_for, session as flask_session
from models import db, ChatSession, ChatMessage, Feedback
from model_runner import generate_response
import os

app = Flask(__name__)
app.secret_key = "replace-this-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
feedback_data = []  # TEMP: For now, in-memory list. We can replace with DB later.

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get or create session ID
    session_id = flask_session.get('session_id')
    if not session_id:
        new_session = ChatSession()
        db.session.add(new_session)
        db.session.commit()
        session_id = new_session.id
        flask_session['session_id'] = session_id

    # Only fetch visible messages
    chat_history = ChatMessage.query.filter_by(
        session_id=session_id, visible=True
    ).order_by(ChatMessage.timestamp).all()

    reply = None
    user_input = None

    if request.method == 'POST':
        # Save user input
        user_input = request.form['message']
        db.session.add(ChatMessage(session_id=session_id, role='user', text=user_input))

        # Generate and save AI reply
        reply = generate_response(user_input)
        db.session.add(ChatMessage(session_id=session_id, role='ai', text=reply))

        db.session.commit()

        # Refresh visible messages after new post
        chat_history = ChatMessage.query.filter_by(
            session_id=session_id, visible=True
        ).order_by(ChatMessage.timestamp).all()

    return render_template(
        'index.html',
        chat_history=chat_history,
        reply=reply,
        user_input=user_input
    )


@app.route('/feedback', methods=['POST'])
def feedback():
    session_id = flask_session.get('session_id')
    if session_id:
        rating = int(request.form['rating'])
        comment = request.form.get('comment', '')
        message_text = request.form.get('message')
        # Get the last AI message in that session
        ai_msg = ChatMessage.query.filter_by(session_id=session_id, role='ai').order_by(ChatMessage.timestamp.desc()).first()
        feedback = Feedback(session_id=session_id, message_id=ai_msg.id if ai_msg else None, rating=rating, comment=comment)
        db.session.add(feedback)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear')
def clear_chat():
    session_id = flask_session.get('session_id')
    if session_id:
        ChatMessage.query.filter_by(session_id=session_id).update({'visible': False})
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/restore')
def restore_chat():
    session_id = flask_session.get('session_id')
    if session_id:
        ChatMessage.query.filter_by(session_id=session_id).update({'visible': True})
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
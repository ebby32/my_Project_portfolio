from flask import render_template, jsonify
from sqlalchemy import false

from application.messages import messages_bp
from application.extensions import db
from application.messages.models import Messages


@messages_bp.route('/messages', methods = ['GET','POST'])
def messages():
    messages_list = db.session.execute(db.select(Messages).order_by(Messages.created_at.desc())).scalars().all()
    return render_template('messages.html', messages = messages_list)


@messages_bp.route("/messages/<int:message_id>/read", methods=["POST"])
def get_message(message_id):
    message = db.session.get(Messages, message_id)

    if not message:
        return jsonify({"error": "Message not found"}), 404

    if not message.is_read:
        message.is_read = True
        print(type(message.is_read), message.is_read)
        db.session.commit()

    return jsonify({"body": message.message or ""})

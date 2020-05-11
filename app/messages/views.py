from app import db

from app.messages.forms import MessageForm
from app.messages.models import Message, UserMessage
from app.messages.utils import send_broadcast_messages

from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, Markup, flash
from flask_login import current_user, login_required

from sqlalchemy import or_

messages = Blueprint('messages', __name__, template_folder='templates')


@messages.route('/messages', defaults={'message_type': 0, 'id': None})
@messages.route('/messages/<int:message_type>/<int:id>')
@login_required
def view_messages(message_type=None, id=None):
    # Message types: 0 - Broadcast Message, 1 - Private Message, 2 - Prayer Request
    if message_type == 0:
        messages_title = "Broadcast Messages"
        messages = db.session.query(Message) \
            .filter(Message.message_type == message_type) \
            .order_by(Message.created_at.desc()).all()
    elif message_type == 1:
        messages_title = "Your private messages"
        messages = db.session.query(Message).join(UserMessage) \
            .filter(Message.message_type == message_type) \
            .filter(or_(UserMessage.user_id == id, Message.created_by == current_user.id)) \
            .order_by(Message.created_at.desc()).all()
    elif message_type == 2:
        messages_title = "Prayer Requests"
        messages = db.session.query(Message) \
            .filter(Message.message_type == message_type) \
            .order_by(Message.created_at.desc()).all()

    return render_template('messages.html', messages_title= messages_title, messages=messages, message_type=message_type)


# @messages.route('/messages/view_message/<int:id>', methods=['GET'])
# @login_required
# def view_message(id):
#     message = Message.query.get(id)
#     return render_template('view_message.html', message=message)

@messages.route('/messages/create_message', defaults={'message_type': 0}, methods=['GET', 'POST'])
@messages.route('/messages/create_message/<int:message_type>', methods=['GET', 'POST'])
@login_required
def create_message(message_type):
    print(f'Received value {message_type}')
    form = MessageForm()
    if form.validate_on_submit():
        message = Message()
        form.populate_obj(message)
        message.created_by = current_user.id
        message.message_type = message_type
        message.created_at = datetime.datetime.utcnow()
        db.session.add(message)
        db.session.commit()
        message_id = message.id
        if form.is_urgent.data:
            send_broadcast_messages(message_id)
        return redirect(url_for('messages.view_messages', message_type=message_type, id=current_user.id))
    return render_template('create_message.html', message_type=message_type, form=form)


@messages.route('/messages/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_message(id):
    message = Message.query.get(id)
    form = MessageForm()
    if request.method == 'GET':
        form = MessageForm(obj=message)
    if form.validate_on_submit():
        form.populate_obj(message)
        db.session.commit()
        if message.message_type == 1:
            return redirect(url_for('messages.view_messages', message_type=1, id=current_user.id))
        return redirect(url_for('messages.view_messages', message_type=0, id=message.created_by))

    return render_template('edit_message.html', form=form)

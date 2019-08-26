from app import db

from app.messages.forms import MessageForm
from app.messages.models import Message, UserMessage
from app.messages.utils import send_broadcast_messages

from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required


messages = Blueprint('messages', __name__, template_folder='templates')


@messages.route('/messages', defaults={'private': 0, 'id': None})
@messages.route('/messages/<int:private>/<int:id>')
def view_messages(private=None, id=None):
    if private:
        if id != current_user.id:
            messages = db.session.query(Message).join(UserMessage) \
                .filter(Message.is_private)\
                .filter(UserMessage.user_id == current_user.id)\
                .filter(Message.created_by == id)\
                .order_by(Message.created_at.desc()).all()
        else:
            messages = db.session.query(Message).join(UserMessage)\
                .filter(Message.is_private)\
                .filter(UserMessage.user_id == current_user.id)\
                .order_by(Message.created_at.desc()).all()
    else:
        if id:
            messages = db.session.query(Message).filter(Message.is_private ==  False)\
                .filter(Message.created_by == id)\
                .order_by(Message.created_at.desc()).all()
        else:
            messages = db.session.query(Message).filter(Message.is_private == False)\
                .order_by(Message.created_at.desc()).all()
    return render_template('messages.html', messages=messages, private=private)


@messages.route('/messages/view_message/<int:id>', methods=['GET'])
@login_required
def view_message(id):
    message = Message.query.get(id)
    return render_template('view_message.html', message=message)


@messages.route('/messages/create_message', methods=['GET', 'POST'])
@login_required
def create_message():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message()
        form.populate_obj(message)
        message.created_by = current_user.id
        db.session.add(message)
        db.session.commit()
        message_id = message.id
        if form.is_urgent.data:
            send_broadcast_messages(message_id)
        return redirect(url_for('messages.view_messages'))
    return render_template('create_message.html', form=form)


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
        if message.is_private:
            return redirect(url_for('messages.view_messages', private=1, id=current_user.id))
        return redirect(url_for('messages.view_messages', private=0, id=message.created_by))

    return render_template('edit_message.html', form=form)


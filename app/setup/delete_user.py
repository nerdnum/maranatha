from app import create_app
from app import db
from app.users.models import User
from app.messages.models import Message, UserMessage


def delete_user(user_id):
    user = User.query.get(user_id)

    statement = Message.__table__.delete().where(Message.created_by == user.id)
    db.session.execute(statement)
    db.session.commit()

    statement = UserMessage.__table__.delete().where(UserMessage.user_id == user.id)
    db.session.execute(statement)
    db.session.commit()

    db.session.delete(user)
    db.session.commit()

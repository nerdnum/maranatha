from app import create_app
from app import db
from app.messages.models import Message
import codecs
from random import randint
from app.users.models import User
from datetime import timedelta, datetime


def upload_verses():
    # app = create_app()

    path = "E:\\Dropbox\\FlaskProjects\\maranatha\\app\\setup\\verses.txt"

    users = User.query.all()

    with codecs.open(path, 'r', 'utf-8') as verses:
        lines = verses.readlines()
        line_iter = iter(lines)
        while True:
            try:
                text = next(line_iter).strip()
                verse = next(line_iter).strip()
                next(line_iter).strip()
                user = users[randint(0, len(users)-1)]
                delta = timedelta(days=randint(0,60), hours=randint(0,23), minutes=randint(0,60))
                time = datetime.utcnow() - delta
                message = Message(subject=text, content=verse, created_by=user.id, created_at=time)
                db.session.add(message)
                print(text, verse)
            except StopIteration:
                break
        db.session.commit()


if __name__ == "__main__":
    upload_verses()

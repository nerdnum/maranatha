from celery import Celery
import time

app = Celery('tasks', backend='db+postgresql://m_user:Pajamas1@localhost:5432/maranatha',
             broker='pyamqp://guest@localhost//')
             


@app.task
def reverse(string):
    time.sleep(10)
    return string[::-1]

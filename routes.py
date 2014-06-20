#!flask/bin/python

from flask import Flask, render_template, send_from_directory
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
#from models import Question
import models

app = Flask(__name__)

app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)

db = MongoEngine(app)
#db.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    text = 'Whooo I am a webpage!!!  Here is a question, and an answer box, and a nav bar.'
    q2 = models.Question(text='Where am I?')
    q2.save()
    questions = models.Question.objects
    print 'questions', questions
    return render_template('index.html', text = text, questions = questions)

@app.route('/prompt')
def prompt():
    text = 'I am a prompt where you can answer the question'
    return render_template('index.html', text = text)

@app.route('/favorites')
def favorites():
    text = 'These are a few of your favorite things.'
    return render_template('index.html', text = text)

@app.route('/answer')
def answer():
    text = 'This is one specific answer in detail'
    return render_template('index.html', text = text)

@app.route('/question')
def question():
    text = 'This is an old question and its answers and stuff'
    return render_template('index.html', text = text)

if __name__ == '__main__':
    app.run()
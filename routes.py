#!flask/bin/python

from flask import Flask, render_template, send_from_directory, request
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
import models
import config

app = Flask(__name__)

app.config["MONGODB_DB"] = config.DB_NAME
connect(config.DB_NAME, host='mongodb://' + config.DB_USERNAME + ':' + config.DB_PASSWORD + '@' + config.DB_HOST_ADDRESS)

db = MongoEngine(app)

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    text = 'Whooo I am a webpage!!!  Here is a question, and an answer box, and a nav bar.'
    if request.method == 'POST':
        print 'post'
        answer=request.form['ans']
        a2 = models.Answer(body=answer)
        a2.save()
    # q2 = models.Question(text='Where am I?')
    # q2.save()
    question = list(models.Question.objects)[-1]
    print 'question', question, list(question)
    answers = models.Answer.objects
    print 'answers', answers
    return render_template('index.html', text = text, 
        question = question, answers = answers)

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
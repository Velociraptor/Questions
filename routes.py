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
    question = list(models.Question.objects)[0]
    if request.method == 'POST':
        answer=request.form['ans']
        a2 = models.Answer(body=answer, question=question)
        a2.save()
    
    answers = models.Answer.objects(question=question)
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

@app.route('/previous', methods=['GET'])
def previous():
    prev_qs = models.Question.objects()
    return render_template('previous.html', questions = prev_qs)

@app.route('/question')
def question(question):
    text = 'This is an old question and its answers and stuff'
    answers = models.Answer.objects(question=question)
    return render_template('index.html', text = text)

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        new_question=request.form['question']
        q = models.Question(text=new_question)
        q.save()
    questions = list(models.Question.objects)[0:10]
    return render_template('admin.html', questions = questions)

if __name__ == '__main__':
    app.run()
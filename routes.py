#!flask/bin/python

from flask import Flask, render_template, send_from_directory, request
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine
from flask.ext.social import Social, MongoEngineConnectionDatastore
from flask.ext.login import LoginManager
import models
import config

app = Flask(__name__)

app.config["MONGODB_DB"] = config.DB_NAME
app.config["SOCIAL_TWITTER"] = {
    'consumer_key': config.twitter_key,
    'consumer_secret': config.twitter_secret
}
connect(config.DB_NAME, host='mongodb://' + config.DB_USERNAME + ':' + config.DB_PASSWORD + '@' + config.DB_HOST_ADDRESS)

db = MongoEngine(app)
#Social(app, MongoEngineConnectionDatastore(db, models.Connection))

login_manager = LoginManager()
login_manager.init_app(app)

def get_current_question():
    return list(models.Question.objects)[0]

def get_answers(question):
    return models.Answer.objects(question=question)

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
#@login_required
def index():
    twitter_conn=social.twitter.get_connection()
    text = 'Whooo I am a webpage!!!  Here is a question, and an answer box, and a nav bar.'
    question = get_current_question()
    if request.method == 'POST':
        answer=request.form['ans']
        a2 = models.Answer(body=answer, question=question)
        a2.save()
        # automatically add answer to user's favorites
    answers = get_answers(question)
    return render_template('index.html', text = text, 
        question = question, answers = answers)

# @login_manager.user_loader
# def load_user(userid):
#     return models.User.objects(uid=userid)[0]

@app.route('/login', methods=['POST'])
def login():
    username=request.form['username']
    print 'username is ', username
    try:
        user = models.User.objects(uname=username)[0]
    except IndexError:
        user = models.User(uname=username)
        user.save()
    # current_user = the person who just logged in

    text = 'Welcome %s. You have successfully logged in!' %username
    question = get_current_question()
    answers = get_answers(question)
    return render_template('index.html', text = text, 
        question = question, answers = answers)

    # do some authentication-y stuff

        # login_user(user)
        # flash("Logged in successfully.")
        # return redirect(request.args.get("next") or url_for("index"))

@app.route('/prompt')
def prompt():
    text = 'I am a prompt where you can answer the question'
    return render_template('index.html', text = text)

@app.route('/favorites')
def favorites():
    text = 'These are a few of your favorite things.'
    # get current user's favorites list
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
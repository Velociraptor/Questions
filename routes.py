#!flask/bin/python

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    text = 'Whooo I am a webpage!!!  Here is a question, and an answer box, and a nav bar.'
    return render_template('index.html', text = text)

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
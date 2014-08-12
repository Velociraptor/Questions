import datetime
from flask import url_for
from routes import db

class Question(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    text = db.StringField(required=True)
    #comments = db.ListField(db.ReferenceField(Comment))

    def __unicode__(self):
        return self.text

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }

class Answer(db.Document):
    question = db.ReferenceField(Question)
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(required=True)

    def __unicode__(self):
        return self.body

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }

class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    uname = db.StringField(required=True)
    #uid = db.IntField(required=True)
    favorites = db.ListField(db.ReferenceField(Answer))

    def __unicode__(self):
        return self.uname

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at'],
        'ordering': ['-created_at']
    }

class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)

def get_question_from_db(created_at):
    if not created_at:
        raise ValueError()
    questions_found = Question.objects(created_at=created_at)
    if len(questions_found) == 1:
        return questions_found[0]
    elif len(questions_found) == 0:
        return None
    else:
        raise Exception('Database Integrity Error')

def get_answers_from_db(question_created_at):
    if not question_created_at:
        raise ValueError()
    answers_found = Answer.objects
    if len(answers_found) > 0:
        return answers_found
    else:
        return None
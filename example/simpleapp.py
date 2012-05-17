from __future__ import with_statement

import datetime
import flask

from random import choice

from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
from flask_debugtoolbar import DebugToolbarExtension

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config['MONGODB_DB'] = 'testing'
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'flask+mongoengine=<3'
app.debug = True
app.config['DEBUG_TB_PANELS'] = (
             'flask_debugtoolbar.panels.versions.VersionDebugPanel',
             'flask_debugtoolbar.panels.timer.TimerDebugPanel',
             'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
             'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
             'flask_debugtoolbar.panels.template.TemplateDebugPanel',
             'flask_debugtoolbar.panels.logger.LoggingPanel',
             'flask_mongoengine.panels.MongoDebugPanel'
             )

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db = MongoEngine()
db.init_app(app)

DebugToolbarExtension(app)


class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now)

@app.route('/')
def index():
    # As a list to test debug toolbar
    Todo.objects().delete()  # Removes
    Todo(title="Simple todo A", text="12345678910").save()  # Insert
    Todo(title="Simple todo B", text="12345678910").save()  # Insert
    Todo.objects(title__contains="B").update(set__text="Hello world")  # Update
    todos = list(Todo.objects[:10])
    todos = Todo.objects.all()
    return flask.render_template('index.html', todos=todos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
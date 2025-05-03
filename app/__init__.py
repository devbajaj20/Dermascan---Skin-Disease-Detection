from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'app/static/uploads'
app.secret_key = 'a7f93b6d4f3928c9408e54bc123c9f1e'

from app import routes  # This should come last after defining `app`

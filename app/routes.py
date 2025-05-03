from flask import render_template, request
from werkzeug.utils import secure_filename
from app import app
import torch
from PIL import Image
import torchvision.transforms as T
import os
import sqlite3
import numpy as np
from flask import session
from flask import Flask, redirect, url_for
app.config['UPLOAD_FOLDER'] = 'static/uploads'


# Load your trained model here
model_path = 'skin-model-pokemon.pt'  # adjust path if needed
torch_model = torch.load('skin-model-pokemon.pt', map_location='cpu', weights_only=False)
torch_model.eval()


def predict(model, img, tr, classes):
    img_tensor = tr(img)
    out = model(img_tensor.unsqueeze(0))
    pred, idx = torch.max(out, 1)
    return classes[idx]

def get_transforms():
    return T.Compose([
        T.Resize((512, 512)),
        T.ToTensor()
    ])

@app.route('/', methods=['GET', 'POST'])
def home_page():
    res = None
    if request.method == 'POST':
        classes = ['warts',
 'vitiligo',
 'acne-scars',
 'acne',
 'oily skin',
 'acanthosis-nigricans',
 'dry skin',
 'melasma',
 'alopecia-areata']

        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_PATH'], filename)

            if not os.path.exists(app.config['UPLOAD_PATH']):
                os.makedirs(app.config['UPLOAD_PATH'])

            file.save(path)

            image = Image.open(path).convert('RGB')
            tr = get_transforms()

            # model must be loaded above this route OR globally
            res = predict(torch_model, image, tr, classes)


    return render_template('index.html', res=res)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    number = request.form.get('number')
    message = request.form.get('message')

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL,
                        number TEXT NOT NULL,
                        message TEXT NOT NULL
                    )''')
    cursor.execute("INSERT INTO messages (name, email, number, message) VALUES (?, ?, ?, ?)",
                   (name, email, number, message))
    conn.commit()
    conn.close()

    return render_template('index.html', success=True)

@app.route('/messages')
def view_messages():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, number, message FROM messages")
    messages = cursor.fetchall()
    conn.close()
    return render_template('messages.html', messages=messages)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", 
                            (username,)).fetchone()

        if user:
            error = "User already registered. Please login."
            conn.close()
        else:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                         (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))

    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['user'] = username
            return redirect(url_for('index'))  # or dashboard
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function

from flask import render_template, redirect, url_for, session
from app import app

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

keras_model = load_model('models/skin_disease_model.h5')  # .h5 model
class_labels = ['Bullous', 'Eczema', 'Herpes', 'Psoriasis', 'Rosacea', 'Warts']

def preprocess_image(image_file):
    img = Image.open(image_file)
    img = img.resize((224, 224))          # Resize to what model expects
    img = img.convert('RGB')              # Ensure 3 channels
    img_array = np.array(img) / 255.0     # Normalize to [0, 1]
    img_array = np.expand_dims(img_array, axis=0)  # Shape becomes (1, 224, 224, 3)
    return img_array

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join('static/uploads', filename)
            file.save(filepath)

            img = preprocess_image(filepath)  # Process the saved image
            prediction = keras_model.predict(img)
            predicted_index = np.argmax(prediction)
            predicted_class = class_labels[predicted_index]
            confidence = prediction[0][predicted_index] * 100

            return render_template('result.html',
                                   prediction=predicted_class,
                                   confidence=round(confidence, 2),
                                   image_path=filepath)
    return render_template('detect.html')
from flask import Flask
app = Flask(__name__)

@app.route('/')
def render_page():
    return render_template('page.html')

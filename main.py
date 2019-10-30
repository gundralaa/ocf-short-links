from flask import Flask
from flask import render_template
from flask import request
import configparser
from ocflib.misc.shorturls import add_shorturl
from ocflib.misc.shorturls import delete_shorturl
from ocflib.misc.shorturls import get_connection as shorturl_db
from ocflib.misc.shorturls import get_shorturl
from ocflib.misc.shorturls import rename_shorturl
from ocflib.misc.shorturls import replace_shorturl
app = Flask(__name__)

@app.route('/')
def render_page():
    return render_template('page.html', success=None)

@app.route('/addUrl', methods=['POST'])
def add_url():
    original_url = request.form['urlInput']
    new_name = request.form['nameInput']
    config = configparser.ConfigParser()
    config.read('pass.ini')
    password = config['mysql']['password']

    if len(new_name) > 100:
        return render_template('page.html', success='New name too long')

    with shorturl_db(user='ocfircbot', password=password) as ctx:
        try:
            add_shorturl(ctx, new_name, original_url)
        except:
            return render_template('page.html', success='Already exists')
        else:
            return render_template('page.html', success='Added')

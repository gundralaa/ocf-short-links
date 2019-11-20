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
    return render_template('page.html', success=None, search_results=[])

@app.route('/', methods=['POST'])
def add_url():
    original_url = request.form['urlInput']
    new_name = request.form['nameInput']
    
    password = pass_extract()

    if len(new_name) > 100:
        return render_template('page.html', success='New name too long')

    with shorturl_db(user='ocfircbot', password=password) as ctx:
        try:
            add_shorturl(ctx, new_name, original_url)
        except:
            return render_template('page.html', success='Error')
        else:
            return render_template('page.html', success='Added')

    return render_template('page.html', success='Error', search_results=[])

@app.route('/find', methods=['POST'])
def search_url():
    query = request.form['searchInput']

    password = pass_extract()

    with shorturl_db(user='ocfircbot', password=password) as ctx:
        try:
            target = get_shorturl(ctx, query)
        except:
            return render_template('page.html', success='Error')
        else:
            target = target if target else "No defined shortlink"
            search_results = [{'name' : query, 'url' : target}]
            return render_template('page.html', success=None, search_results=search_results)

    return render_template('page.html', success='Error')

@app.route('/delete/<query>', methods=['POST'])
def delete_url(query=None):

    password = pass_extract()

    with shorturl_db(user='ocfircbot', password=password) as ctx:
        try:
            delete_shorturl(ctx, query)
        except:
            return render_template('page.html', success='Error')
        else:
            return render_template('page.html', success='Deleted', search_results=[])

    return render_template('page.html', success='Error')


def pass_extract():
    
    config = configparser.ConfigParser()
    path = '../pass/irc-bot.conf'
    config.read(path)
    password = config['mysql']['password']
    
    return password

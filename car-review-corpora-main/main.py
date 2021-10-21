import sqlite3
import searcher
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
con = sqlite3.connect('tachka_database.db', check_same_thread=False)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/search', methods=['get'])
def searching():
    if not request.args:
        return redirect(url_for('main'))
    s = request.args.get('query')
    u = searcher.search(s, con, searcher.ms)
    ll = searcher.sents(u, con)
    return render_template('search.html', ll=ll)


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/tagset')
def tagset():
    return render_template('tagset.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.errorhandler(500)
def error_500(e):
    return render_template('500.html')


if __name__ == '__main__':
    app.run()

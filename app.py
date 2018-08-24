from flask import Flask, render_template
from persianvocalizer import HMMVocalizer

app = Flask(__name__, static_url_path='/static')

vocalizer = HMMVocalizer()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/vocalization/<string:transliterated>')
def vocalize(transliterated):
    return vocalizer.vocalize(transliterated)


if __name__ == '__main__':
    app.run()

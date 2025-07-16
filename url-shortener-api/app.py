from flask import Flask, render_template
from routes.url_route import url_blueprint
from config import mongo

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['MONGO_URI'] = mongo

app.register_blueprint(url_blueprint)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/r/<short_code>')
def redirect_page(short_code):
    return render_template('redirect.html', short_code=short_code)

if __name__ == '__main__':
    app.run(debug=True)

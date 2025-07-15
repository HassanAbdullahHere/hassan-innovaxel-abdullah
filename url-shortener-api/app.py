from flask import Flask
from routes.url_route import url_blueprint
from config import mongo

app = Flask(__name__)
app.config['MONGO_URI'] = mongo
app.register_blueprint(url_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

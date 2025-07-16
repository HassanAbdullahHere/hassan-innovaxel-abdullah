from flask import Flask, render_template
from routes.url_route import url_blueprint
from config import mongo

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['MONGO_URI'] = mongo

# Register routes
app.register_blueprint(url_blueprint)

# Serve index.html at root
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

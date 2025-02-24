from flask import Flask
from routes import upload_blueprint
from database import init_db

app = Flask(__name__)
app.register_blueprint(upload_blueprint)

init_db()

if __name__ == '__main__':
    app.run(debug=True)

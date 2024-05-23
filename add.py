from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db, bcrypt
from routes import bp
from config import Config
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)

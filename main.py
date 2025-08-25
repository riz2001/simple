from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)


# Database URL (change later for Render cloud DB)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL",   # Read from environment
    "postgresql://postgres:@localhost:5432/keralastate"  # fallback, safe (no password)
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)  # added email

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    return "Flask + PostgreSQL App is Running!"

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email} for u in users])

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = User(name=data["name"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added!"})

@app.route("/home")
def home_page():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

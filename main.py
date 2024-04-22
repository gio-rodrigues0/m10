from flask import Flask
from database.database import db
from flask import jsonify, request, render_template, make_response
from database.models import User, Tasks
import sys
from flask_jwt_extended import JWTManager, set_access_cookies
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests as http_request

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db.init_app(app)

app.config["JWT_SECRET_KEY"] = "giovanna-linda" 

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)

if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    # cria o banco de dados
    with app.app_context():
        db.create_all()
    # Finaliza a execução do programa
    print("Database created successfully")
    sys.exit(0)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=username, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })
    
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("email", None)
    password = request.json.get("password", None)
    # Verifica os dados enviados não estão nulos
    if username is None or password is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    # faz uma chamada para a criação do token
    token_data = http_request.post("http://localhost:5000/token", json={"username": username, "password": password})
    if token_data.status_code != 200:
        return jsonify({"msg": "Bad username or password"}), 401
    # recupera o token
    response = make_response(render_template("index.html"))

    set_access_cookies(response, token_data.json()['token'])

    return response

@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    return_users = []
    for user in users:
        return_users.append(user.serialize())
    return jsonify(return_users)

@app.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize())

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
    data = request.json
    user = User.query.get(id)
    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    tasks = Tasks.query.all()
    return_tasks = []
    for task in tasks:
        return_tasks.append(task.serialize())
    return jsonify(return_tasks)

@app.route("/tasks/<int:id>", methods=["GET"])
@jwt_required()
def get_task(id):
    task = Tasks.query.get(id)
    return jsonify(task.serialize())

@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    data = request.json
    task = Tasks(description=data["description"])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.serialize())

@app.route("/tasks/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    data = request.json
    task = Tasks.query.get(id)
    task.name = data["description"]
    db.session.commit()
    return jsonify(task.serialize())

@app.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    task = Tasks.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(task.serialize())

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from utils.token import create_access_token, verify_token

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        login_ = request.form["login"]
        pwd = request.form["password"]
        user = User.query.filter_by(login=login_, password=pwd).first()
        if user is not None:
            access_token = create_access_token(login_, pwd)
            user.token = access_token
            db.session.add(user)
            db.session.commit()
            return f"<h1>token: {access_token}</h1>"
        else:
            return f"<h1>Could not found a user with login: {login_}</h1>"


@app.route("/protected", methods=["GET"])
def protected():
    encoded_jwt = request.args.get("token")
    decoded_jwt = verify_token(encoded_jwt)
    if decoded_jwt:
        login_ = decoded_jwt.get("login")
        pwd = decoded_jwt.get("password")
        user = User.query.filter_by(login=login_, password=pwd).first()
        if user is not None:
            return "<h1>Hello, token which is provided is correct </h1>"
    return "<h1>Hello, Could not verify the token</h1>"


if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run(host="0.0.0.0", port=5000)

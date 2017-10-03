#UTF-8
from flask import Flask, render_template, request, url_for, redirect

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:boladebola@localhost/ultima_vez'

db = SQLAlchemy(app)

SQLALCHEMY_TRACK_MODIFICATIONS = True

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    senha = db.Column(db.String(16))
    email = db.Column(db.String(50), unique=True)

    def __init__(self,senha,email):
        self.senha = senha
        self.email = email

db.create_all()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/logged")
def logged():
    return render_template("logged.html")



@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        senha = (request.form.get("senha"))
        email = (request.form.get("email"))

        new_user = User(senha=senha,email=email)
        db.session.add(new_user)
        db.session.commit(new_user)
        return redirect(url_for("index"))



@app.route("/checklogin", methods=['POST'])
def check():
    senha = (request.form.get("senha"))
    email = (request.form.get("email"))
    user = User.query.filter_by(email=email).first()
    if user is not None:
        if user.senha == senha:
            return redirect(url_for("logged"))
        else :
            return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)

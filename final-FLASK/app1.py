#UTF-8
import sys
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user


app = Flask(__name__)

app.config.from_object('config')


db = SQLAlchemy(app)


lm = LoginManager()
lm.init_app(app)


@lm.user_loader
def load_user(id):
    return User.get(id)


import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    value = StringField("value", validators=[DataRequired()])

class products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    value = db.Column(db.Integer)

    def __init__(self,name,description,value):
        self.name = name
        self.description = description
        self.value  = value

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    senha = db.Column(db.String(16))
    email = db.Column(db.String(50), unique=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


    def __init__(self,senha,email):
        self.senha = senha
        self.email = email

db.create_all()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# user = User.query.filter_by(email=form.emai.data).first()
 #        if user and user.senha == form.senha.data:
  #          login_user(user)
   #         flash("logado com sucesso")
    #    else:
     #       flash("login invalido")



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user is not None:
        if user.senha == form.senha.data:
            flash("Usuario logado com sucesso")
            return redirect(url_for("logged"))
        else :
            flash("login invalido")
            return redirect(url_for("index"))
    return render_template("login.html",form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = LoginForm()
    if request.method == 'POST':
        senha = (request.form.get("senha"))
        email = (request.form.get("email"))
        new_user = User(senha=senha,email=email)
        
        db.session.add(new_user)
        db.session.commit()
        flash("Usuario Cadastrado com Sucesso")
    return render_template("signup.html",form=form)



@app.route("/logged", methods=['GET', 'POST'])
def logged():
    form = LoginForm()
    if request.method == 'POST':
        name = (request.form.get("name"))
        description = (request.form.get("description"))
        value = (request.form.get("value"))
        new_product = products(name=name,description=description,value=value)
        
        db.session.add(new_product)
        db.session.commit()
        flash("Item criado com sucesso")
    return render_template("logged.html", form=form)



@app.route("/contact")
def contato():
    return render_template("contact.html")

@app.route("/create", methods=['GET'])
def create():
    form = LoginForm()
    produtos = products.query.all()
    return render_template("create.html",produtos=produtos)


    
@app.route("/logout")
def logout():
    logout_user()
    flash("Deslogado com sucesso")
    return redirect(url_for("index.html"))

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session, url_for 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "your secrete key"


# database mode: a row of data 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myusers.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password_hash = db.Column(db.String(125), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# home page
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template("index.html")


# login page  
@app.route("/login", methods=["POST"])
def login():
    # collect informaton
    username = request.form["username"]
    password = request.form["password"]

    # check if its in the db
    user= User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    # otherwise show home page
    else:
        return render_template("index.html")

 


# register page 
@app.route("/register", methods=["POST"])
def register():
    username= request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", error="user already here!")
    else:
        new_user = User(username=username )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        session['username']= username

        return redirect(url_for("dashboard"))
    

# Dashboard page 
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html", username=session["username"])

    return redirect(url_for('home'))


# logout page
["bob", "champ", "josh"]
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for("home"))


if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)


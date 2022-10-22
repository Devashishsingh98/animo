from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

"""" CREATING APP AND DATABASE"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# ______________________________________________________________________________________

"""DATABASE INITIATION"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)


# _________________________________________________________________________________________
""" Display All Users in list"""


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


# ___________________________________________________________________________________________

""" CREATE USERS """


@app.route("/users", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/")
# _____________________________________________________________________________________________


""" DELETE USERS ID"""


@app.route("/delete", methods=["GET", "POST"])
def user_delete():
    if request.method == "POST":
        user = User.query.get(request.form["name"])
        db.session.delete(user)
        db.session.commit()
        return redirect("/")
# _____________________________________________________________________________________________


""" RUNNING APP AND DB CREATION """
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

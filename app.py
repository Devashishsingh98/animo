from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy

"""" CREATING APP AND DATABASE"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
db = SQLAlchemy(app)
# ______________________________________________________________________________________

"""DATABASE INITIATION"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)

    def __init__(self, name, email):
        self.name = name
        self.email = email
# _________________________________________________________________________________________


""" LIST OF USERS """


@app.route("/users")
def user_list():
    users = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html")
# ___________________________________________________________________________________________


""" CREATE USERS """


@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")
# _____________________________________________________________________________________________


"""GET USERS DETAIL"""


@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)
# _____________________________________________________________________________________________


""" DELETE USERS ID"""


@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)
# _____________________________________________________________________________________________


""" RUNNING APP AND DB CREATION """
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

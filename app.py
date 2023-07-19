from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

import DummyData

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:kaku@localhost/dummy"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    phone = db.Column(db.String(10), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)


# homepage route
@app.route('/')
def home_page():  # put application's code here
    return render_template('home.html')


# user routes
@app.route('/booking')
def booking_page():
    return render_template("booking.html")


@app.route('/busroute')
def bus_routes_page():
    return render_template("busroute.html")


@app.route('/login', methods=["GET", "POST"])
def login_account():
    if request.method == "POST":
        return redirect("/booking")
    else:
        return render_template("login.html")


@app.route('/signup', methods=["GET", "POST"])
def signup_account():
    if request.method == "POST":
        return redirect("/booking")
    else:
        return render_template("signup.html")


# admin routes
@app.route('/admin/login', methods=["GET", "POST"])
def admin_login_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin":
            return redirect("/admin")
        return render_template("adminlogin.html")
    else:
        return render_template("adminlogin.html")


@app.route('/admin')
def dashboard_page():
    return render_template("dashboard.html")


@app.route('/admin/users')
def users_page():
    return render_template("users.html", users=DummyData.users)


@app.route('/admin/buslist')
def bus_list_page():
    return render_template("buslist.html", buslist=DummyData.buslist)


@app.route('/admin/employees')
def bus_employees_page():
    return render_template("employee.html", employees=DummyData.employees)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

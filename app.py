from datetime import datetime

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

import DummyData

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:kaku@localhost/dummy"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)


# Database Models

# userno - 5 characters
# employee - 3 characters
# ticket - 8 characters
# bus - 10 characters
# route - 5 characters
# schedule - 5 characters
class User(db.Model):
    user_id = db.Column(db.String(5), primary_key=True)
    user_name = db.Column(db.String(40), unique=False, nullable=False)
    user_age = db.Column(db.Integer, unique=False, nullable=False)
    user_phone = db.Column(db.String(10), unique=True, nullable=False)
    user_email = db.Column(db.String(40), unique=True, nullable=False)
    user_password = db.Column(db.String(20), unique=False, nullable=False)


class Employee(db.Model):
    employee_no = db.Column(db.String(3), primary_key=True)
    employee_name = db.Column(db.String(40), unique=False, nullable=False)
    employee_age = db.Column(db.Integer, unique=False, nullable=False)
    employee_phone = db.Column(db.String(10), unique=True, nullable=False)

    bus = db.relationship('Bus', backref='employee', uselist=False)



class Ticket(db.Model):
    ticket_no = db.Column(db.String(8), primary_key=True)
    ticket_amount = db.Column(db.Integer, unique=False, nullable=False)
    ticket_date = db.Column(db.DateTime, default=datetime.utcnow)
    bus_no = db.Column(db.String(10), db.ForeignKey('bus.bus_no'), unique=False, nullable=False)


class Bus(db.Model):
    bus_no = db.Column(db.String(10), primary_key=True)
    bus_name = db.Column(db.String(50), unique=False, nullable=False)
    employee_no = db.Column(db.String(3), db.ForeignKey('employee.employee_no'), unique=False, nullable=False)
    route_no = db.Column(db.String(50), db.ForeignKey('route.route_no'), unique=False, nullable=False)

    ticket = db.relationship('Ticket', backref='bus', uselist=False)
    schedule = db.relationship('Schedule', backref='bus', lazy=True)


class Route(db.Model):
    route_no = db.Column(db.String(5), primary_key=True)
    from_loc = db.Column(db.String(20), unique=False, nullable=False)
    to_loc = db.Column(db.String(20), unique=False, nullable=False)

    bus = db.relationship('Bus', backref='route', uselist=False)


class Schedule(db.Model):
    schedule_id = db.Column(db.String(5), primary_key=True)
    dept_time = db.Column(db.String(20), nullable=False)
    arr_time = db.Column(db.String(20), nullable=False)
    bus_no = db.Column(db.String(10), db.ForeignKey('bus.bus_no'), unique=False, nullable=False)


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
    routes = Route.query.all()
    routes_data = []
    for route in routes:
        route_data = {
            'routeno': route.route_no,
            'from': route.from_loc,
            'to': route.to_loc,
        }
        routes_data.append(route_data)

    return render_template("busroute.html", routes=routes_data)


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


@app.route('/admin/users', methods=["GET"])
def users_page():
    all_users = User.query.all()
    users_data = []
    for user in all_users:
        user_data = {
            'userno': user.user_id,
            'name': user.user_name,
            'age': user.user_age,
            'phone': user.user_phone,
            'email': user.user_email
        }
        users_data.append(user_data)
    return render_template("users.html", users=users_data)


@app.route('/admin/buslist')
def bus_list_page():
    buslists = Bus.query.all()
    buslists_data = []
    for bus in buslists:
        buslist_data = {
            "BusNo": bus.bus_no,
            "BusName": bus.bus_name,
            "Enumber": bus.employee_no,
            "RouteNo": bus.route_no
        }
        buslists_data.append(buslist_data)
    return render_template("buslist.html", buslist=buslists_data)


@app.route('/admin/employees')
def bus_employees_page():
    employees = Employee.query.all()
    employees_data = []
    for employee in employees:
        employee_data = {
            "Eno": employee.employee_no,
            "Ename": employee.employee_name,
            "Eage": employee.employee_age,
            "Ephone": employee.employee_phone
        }
        employees_data.append(employee_data)
    return render_template("employee.html", employees=employees_data)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

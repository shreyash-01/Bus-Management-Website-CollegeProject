from datetime import datetime

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

import DummyData

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:kaku@localhost/dummy"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://sql6634988:5NwvDdkmqH@sql6.freesqldatabase.com:3306/sql6634988"
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)


# Database Models


class User(db.Model):
    UserNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(40), unique=False, nullable=False)
    Age = db.Column(db.Integer, unique=False, nullable=False)
    Phone = db.Column(db.String(10), unique=True, nullable=False)
    Email = db.Column(db.String(40), unique=True, nullable=False)
    Password = db.Column(db.String(20), unique=False, nullable=False)


class Employee(db.Model):
    ENo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EName = db.Column(db.String(40), unique=False, nullable=False)
    EAge = db.Column(db.Integer, unique=False, nullable=False)
    EPhone = db.Column(db.String(10), unique=True, nullable=False)

    bus = db.relationship('Bus', backref='employee', uselist=False)



class Ticket(db.Model):
    ticket_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_amount = db.Column(db.Integer, unique=False, nullable=False)
    ticket_date = db.Column(db.DateTime, default=datetime.utcnow)
    BusNo = db.Column(db.Integer, db.ForeignKey('bus.BusNo'), unique=False, nullable=False)


class Bus(db.Model):
    BusNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    busname = db.Column(db.String(50), unique=False, nullable=False)
    ENo = db.Column(db.Integer, db.ForeignKey('employee.ENo'), unique=False, nullable=False)
    RouteNo = db.Column(db.Integer, db.ForeignKey('route.RouteNo'), unique=False, nullable=False)

    ticket = db.relationship('Ticket', backref='bus', uselist=False)
    schedule = db.relationship('Schedule', backref='bus', lazy=True)


class Route(db.Model):
    RouteNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SourceLocation = db.Column(db.String(20), unique=False, nullable=False)
    DestinationLocation = db.Column(db.String(20), unique=False, nullable=False)

    bus = db.relationship('Bus', backref='route', uselist=False)


class Schedule(db.Model):
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dept_time = db.Column(db.String(20), nullable=False)
    arr_time = db.Column(db.String(20), nullable=False)
    BusNo = db.Column(db.Integer, db.ForeignKey('bus.BusNo'), unique=False, nullable=False)


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
            'routeno': route.RouteNo,
            'from': route.SourceLocation,
            'to': route.DestinationLocation,
        }
        routes_data.append(route_data)

    return render_template("busroute.html", routes=routes_data)


@app.route('/login', methods=["GET", "POST"])
def login_account():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(user_email=email, user_password=password).first()
        if user:
            return redirect("/booking")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route('/signup', methods=["GET", "POST"])
def signup_account():
    if request.method == "POST":
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        user = User(user_name=name,
                    user_age=age,
                    user_gender=gender,
                    user_phone=phone,
                    user_email=email,
                    user_password=password)
        db.session.add(user)
        db.session.commit()
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
            'userno': user.UserNo,
            'name': user.Name,
            'age': user.Age,
            'phone': user.Phone,
            'email': user.Email,
            'password': user.Password
        }
        users_data.append(user_data)
    return render_template("users.html", users=users_data)


@app.route('/admin/buslist')
def bus_list_page():
    buslists = Bus.query.all()
    buslists_data = []
    for bus in buslists:
        buslist_data = {
            "BusNo": bus.BusNo,
            "BusName": bus.busname,
            "Enumber": bus.ENo,
            "RouteNo": bus.RouteNo
        }
        buslists_data.append(buslist_data)
    return render_template("buslist.html", buslist=buslists_data)


@app.route('/admin/employees')
def bus_employees_page():
    employees = Employee.query.all()
    employees_data = []
    for employee in employees:
        employee_data = {
            "Eno": employee.ENo,
            "Ename": employee.EName,
            "Eage": employee.EAge,
            "Ephone": employee.EPhone
        }
        employees_data.append(employee_data)
    return render_template("employee.html", employees=employees_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8000, debug=True)

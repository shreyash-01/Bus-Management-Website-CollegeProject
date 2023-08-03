from datetime import datetime

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://sql6636979:MXn2jrUKbv@sql6.freesqldatabase.com:3306/sql6636979"
db = SQLAlchemy(app)


# Database Models

def generate_ticket_pdf(ticket_details, pdf_filename):
    # Create a PDF using ReportLab
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Assuming you have a dictionary with ticket details
    # For example, ticket_details = {"name": "John Doe", "seat_number": "A12", "bus_details": "Bus XYZ", ...}

    # Write ticket details to the PDF
    c.drawString(100, 750, f"Passenger Name: {ticket_details['busno']}")
    c.drawString(100, 730, f"Seat Number: {ticket_details['busname']}")
    c.drawString(100, 710, f"Bus Details: {ticket_details['from']}")
    c.drawString(100, 810, f"Bus Details: {ticket_details['to']}")
    c.drawString(100, 910, f"Bus Details: {ticket_details['dday']}")
    # Add more details as needed

    c.save()


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
    TicketNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TAmount = db.Column(db.Integer, unique=False, nullable=False)
    TDate = db.Column(db.DateTime, default=datetime.utcnow)
    BusNo = db.Column(db.Integer, db.ForeignKey('bus.BusNo'), unique=False, nullable=False)

    booking = db.relationship('Booking', backref='ticket')



class Bus(db.Model):
    BusNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    busname = db.Column(db.String(50), unique=False, nullable=False)
    ENo = db.Column(db.Integer, db.ForeignKey('employee.ENo'), unique=False, nullable=False)
    RouteNo = db.Column(db.Integer, db.ForeignKey('route.RouteNo'), unique=False, nullable=False)

    ticket = db.relationship('Ticket', backref='bus', uselist=False)
    schedule = db.relationship('Schedule', backref='bus', lazy=True)
    book = db.relationship('Booking', backref='bus', lazy=True)



class Route(db.Model):
    RouteNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SourceLocation = db.Column(db.String(20), unique=False, nullable=False)
    DestinationLocation = db.Column(db.String(20), unique=False, nullable=False)

    bus = db.relationship('Bus', backref='route', uselist=False)

class Booking(db.Model):
    BookingNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TicketNo = db.Column(db.Integer, db.ForeignKey('ticket.TicketNo'), unique=False, nullable=False)
    BusNo = db.Column(db.Integer, db.ForeignKey('bus.BusNo'), unique=False, nullable=False)
    TravelDate = db.Column(db.String(20), unique=False, nullable=False)
    ScheduleID = db.Column(db.String(5), db.ForeignKey('schedule.scheduleid'), unique=False, nullable=False)




class Schedule(db.Model):
    scheduleid = db.Column(db.String(5), primary_key=True, autoincrement=True)
    DepartureTime = db.Column(db.String(20), nullable=False)
    ArrivalTime = db.Column(db.String(20), nullable=False)
    DepartureDay = db.Column(db.String(20), nullable=False)
    BusNo = db.Column(db.Integer, db.ForeignKey('bus.BusNo'), unique=False, nullable=False)

    book = db.relationship('Booking', backref='schedule')



# homepage route
@app.route('/')
def home_page():  # put application's code here
    return render_template('home.html')


# user routes
@app.route('/booking', methods=["GET", "POST"])
def booking_page():
    if request.method == "GET":
        data = db.session.query(Bus.BusNo, Bus.busname, Schedule.DepartureTime, Schedule.DepartureDay, Route.SourceLocation, Route.DestinationLocation).join(Route).join(Schedule).all()
        input_data = []
        for a in data:
            dic = {
                "BusNo": a[0],
                "Name": a[1],
                "DepTime": a[2],
                "DepDay": a[3],
                "From": a[4],
                "To": a[5]
            }
            input_data.append(dic)
            print(dic)
        return render_template("booking.html", data=input_data)
    else:
        data = request.get_json()
        input_data = data["input_data"]
        busno = input_data['busno']
        busname = input_data['busname']
        from_ = input_data['from']
        to = input_data['to']
        dday = input_data['departureday']
        ticket_details = {
            "busno": busno,
            "busname": busname,
            "from": from_,
            "to": to,
            "dday": dday,
            # Add more details here
        }
        pdf_filename = "shreyash_ticket.pdf"  # You can name the PDF as per your requirement
        generate_ticket_pdf(ticket_details, pdf_filename)

        data = db.session.query(Bus.BusNo, Bus.busname, Schedule.DepartureTime, Schedule.DepartureDay,
                                Route.SourceLocation, Route.DestinationLocation).join(Route).join(Schedule).all()
        input_data = []
        for a in data:
            dic = {
                "BusNo": a[0],
                "Name": a[1],
                "DepTime": a[2],
                "DepDay": a[3],
                "From": a[4],
                "To": a[5]
            }
            input_data.append(dic)
        return render_template("booking.html", data=input_data)

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
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        user = User(Name=name,
                    Age=age,
                    Phone=phone,
                    Email=email,
                    Password=password)
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


@app.route('/admin/buslist', methods=["GET", "POST"])
def bus_list_page():
    if request.method == "POST":
        data = request.get_json()
        input_data = data['input_data']
        print(input_data)
        bus = Bus(BusNo=input_data['bno'],
                            busname=input_data['bname'],
                            ENo=input_data['eno'],
                            RouteNo=input_data['rno'])
        db.session.add(bus)
        db.session.commit()
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
    else :
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


@app.route('/admin/employees', methods=["POST", "GET"])
def bus_employees_page():
    if request.method == "POST":
        data = request.get_json()
        input_data = data['input_data']
        employee = Employee(ENo=input_data['eno'],
                            EName=input_data['ename'],
                            EAge=input_data['eage'],
                            EPhone=input_data['ephone'])
        db.session.add(employee)
        db.session.commit()
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
    else :
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

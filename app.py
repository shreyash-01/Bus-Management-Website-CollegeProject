from flask import Flask, render_template
import DummyData
app = Flask(__name__)


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


@app.route('/login')
def login_account():
    return render_template("login.html")


@app.route('/signup')
def signup_account():
    return render_template("signup.html")


# admin routes
@app.route('/admin/login')
def admin_login_page():
    return "this is login page for admin"


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

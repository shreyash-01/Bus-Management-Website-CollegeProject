from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home_page():  # put application's code here
    return render_template('home.html')


@app.route('/account')
def user_account():
    return "this is account page"


@app.route('/login')
def login_account():
    return render_template("login.html")


@app.route('/signup')
def signup_account():
    return render_template("signup.html")


@app.route('/admin/dashboard')
def dashboard_page():
    return render_template("dashboard.html")


@app.route('/admin/users')
def users_page():
    return render_template("users.html")


@app.route('/admin/busroutes')
def bus_routes():
    return render_template("busroute.html")


@app.route('/admin')
def admin_login_page():
    return "this is login page for admin"

@app.route('/booking')
def booking_page():
    return render_template("booking.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

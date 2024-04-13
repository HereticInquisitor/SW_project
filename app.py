from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to authenticate user credentials
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        print(user)
        if user:
            if user[3] == 'user':
                return redirect(url_for('user_dashboard'))
            elif user[3] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user[3] == 'sponsor':
                return redirect(url_for('sponsor_dashboard'))
            else:
                return "Invalid user type"
        else:
            return "Invalid credentials"
    return render_template('login.html')

# Routes for different dashboards
@app.route('/user')
def user_dashboard():
    return "Welcome to user dashboard"

@app.route('/admin')
def admin_dashboard():
    return "Welcome to admin dashboard"

@app.route('/sponsor')
def sponsor_dashboard():
    return "Welcome to sponsor dashboard"

if __name__ == '__main__':
    app.run(debug=True)

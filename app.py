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
    return render_template('user_dashboard.html')

# Route for user registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Process the form data here (e.g., save to database)
        # Redirect to user dashboard after registration
        return redirect(url_for('user_dashboard'))
    return render_template('user_form.html')

@app.route('/book-tickets')
def book_tickets():
    # You can add any necessary logic here
    return render_template('book_tickets.html')

# Route for the admin dashboard
# Route for the admin dashboard
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    # Function to insert event data into the database
    def insert_event(title, description, date):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO events (title, description, date) VALUES (?, ?, ?)", (title, description, date))
        conn.commit()
        conn.close()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        insert_event(title, description, date)
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_dashboard.html')

@app.route('/sponsor')
def sponsor_dashboard():
    return "Welcome to sponsor dashboard"

if __name__ == '__main__':
    app.run(debug=True)

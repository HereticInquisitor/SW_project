from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

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
                return redirect(url_for('sponsor_registration'))
            else:
                return "Invalid user type"
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/user')
def user_dashboard():
    return render_template('user_dashboard.html')

def insert_registration(username, email, fullname, age, gender, phone, address):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO registrations (username, email, fullname, age, gender, phone, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (username, email, fullname, age, gender, phone, address))
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        username = request.form['username']
        email = request.form['email']
        fullname = request.form['fullname']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        
        insert_registration(username, email, fullname, age, gender, phone, address)
        
        return redirect(url_for('user_dashboard'))
    return render_template('user_form.html')

@app.route('/book-tickets')
def book_tickets():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, title FROM events")
    events = c.fetchall()
    conn.close()
    return render_template('book_tickets.html', events=events)
    
def insert_event(title, description, date):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO events (title, description, date) VALUES (?, ?, ?)", (title, description, date))
    conn.commit()
    conn.close()

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/create_event_page')
def create_event_page():
    return render_template('create_event_page.html')

@app.route('/create_event', methods=['POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        insert_event(title, description, date)
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_dashboard.html') 


@app.route('/create_event_form')
def delete_event_form():
    return render_template('delete_event_form.html')

@app.route('/delete_event', methods=['POST','GET'])
def delete_event():
    if request.method == 'POST':
        event_id = request.form['event']
        conn = sqlite3.connect('your_database.db')
        c = conn.cursor()
        c.execute("DELETE FROM events WHERE id=?", (event_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
@app.route('/event_list')
def event_list():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM events")
    events = c.fetchall()
    conn.close()
    return render_template('event_list.html', events=events)


@app.route('/logout')
def logout():
    return redirect(url_for('login'))


def get_total_budget():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT SUM(sponsored_amount) FROM sponsors")
    total_budget_row = c.fetchone()[0]
    total_budget = total_budget_row if total_budget_row is not None else 0
    conn.close()
    return total_budget

@app.route('/budget_management', methods=['GET', 'POST'])
def budget_management():
    if request.method == 'POST':
        marketing = int(request.form['marketing'])
        operations = int(request.form['operations'])
        technology = int(request.form['technology'])
        miscellaneous = int(request.form['miscellaneous'])

        distributed_budget = marketing + operations + technology + miscellaneous

        total_budget = get_total_budget()

        if total_budget < distributed_budget:
            error_message = 'Error: Total budget is less than the distributed budget!'
            return render_template('budget_management.html', total_budget=total_budget, error_message=error_message)
        else:
            remaining_budget = total_budget - distributed_budget


            return redirect(url_for('budget_management'))

    return render_template('budget_management.html', total_budget=get_total_budget())


@app.route('/sponsor_dashboard')
def sponsor_dashboard():

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT name, sponsored_amount FROM sponsors WHERE sponsored_amount > 0")
    sponsors = c.fetchall()

    conn.close()

    return render_template('sponsor_management.html', sponsors=sponsors)


@app.route('/venue_selection')
def venue_selection():

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("SELECT * FROM venues")
    venues = c.fetchall()

    conn.close()

    return render_template('venue_selection.html', venues=venues)



@app.route('/sponsor_registration', methods=['GET', 'POST'])
def sponsor_registration():
    if request.method == 'POST':

        name = request.form['name']
        amount = request.form['amount']
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO sponsors (name, sponsored_amount) VALUES (?, ?)", (name, amount))
        conn.commit()
        conn.close()
        
        return "Thank you"
    
    return render_template('sponsor_registration.html')

if __name__ == '__main__':
    app.run(debug=True)

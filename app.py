from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Hardcoded credentials
USERNAME = 'user'
PASSWORD = 'password'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/calculator', methods=['GET', 'POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        work_hours = {}
        total_hours = 0
        hourly_rate = float(request.form.get('hourly_rate', 0))
        
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            start_time = request.form.get(f'{day}_start', '00:00')
            end_time = request.form.get(f'{day}_end', '00:00')
            
            if start_time and end_time:
                start_hour, start_minute = map(int, start_time.split(':'))
                end_hour, end_minute = map(int, end_time.split(':'))
                
                # Calculate hours worked for the day
                hours_worked = (end_hour + end_minute / 60) - (start_hour + start_minute / 60)
                if hours_worked < 0:  # In case end time is earlier than start time (e.g., night shift)
                    hours_worked += 24
                
                work_hours[day] = round(hours_worked, 2)
                total_hours += hours_worked
        
        total_earnings = total_hours * hourly_rate
        return render_template('index.html', work_hours=work_hours, total_earnings=total_earnings, total_hours=round(total_hours, 2), hourly_rate=hourly_rate)

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

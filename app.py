from flask import Flask, render_template, redirect, session, request
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '5665'

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'ToDoApp'

app.config['MYSQL_HOST'] = 'nilay003.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'nilay003'
app.config['MYSQL_PASSWORD'] = '@Nilay0112'
app.config['MYSQL_DB'] = 'nilay003$ToDoApp'
mysql = MySQL(app)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT Username, Password FROM USERS WHERE Username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[1], password):
            session['Username'] = user[0]
            return redirect('/dashboard')
        else:
            return "Invalid username or password."

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO USERS (Username, FirstName, LastName, Password) VALUES (%s, %s, %s, %s)", (username, firstname, lastname, hashed_password))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
        except Exception as e:
            print(f"Error inserting user: {str(e)}")
            return "Failed to register user."

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'Username' in session:
        username = session['Username']

        cur = mysql.connection.cursor()
        cur.execute("SELECT TaskID, TaskTitle, Description, Status FROM TASK WHERE Username = %s", (username,))
        tasks = cur.fetchall()
        cur.close()

        return render_template('dashboard.html', tasks=tasks)
    else:
        return render_template('dashboard.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        username = session['Username']
        tasktitle = request.form['tasktitle']
        description = request.form['description']
        status = request.form['status']

        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO TASK (Username, TaskTitle, Description, Status) VALUES (%s, %s, %s, %s)", (username, tasktitle, description, status))
            mysql.connection.commit()
            cur.close()
            return redirect('/dashboard')
        except Exception as e:
            print(f"Error adding task: {str(e)}")
            return "Failed to add task."

    return render_template('add.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        username = session['Username']
        taskid = request.form['taskid']
        status = request.form['status']

        cur = mysql.connection.cursor()
        try:
            cur.execute("UPDATE TASK SET Status = %s WHERE TaskID = %s AND Username = %s", (status, taskid, username))
            mysql.connection.commit()
            cur.close()
            return redirect('/dashboard')
        except Exception as e:
            print(f"Error updating task: {str(e)}")
            return "Failed to update task."

    return render_template('update.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        username = session['Username']
        taskid = request.form['taskid']

        cur = mysql.connection.cursor()
        try:
            cur.execute("DELETE FROM TASK WHERE TaskID = %s AND Username = %s", (taskid, username))
            mysql.connection.commit()
            cur.close()
            return redirect('/dashboard')
        except Exception as e:
            print(f"Error removing task: {str(e)}")
            return "Failed to remove task."

    return render_template('remove.html')

@app.route('/logout')
def logout():
    session.pop('Username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

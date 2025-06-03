from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'tamal_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'SchoolMS'

mysql = MySQL(app)

def create_userTables():
    with app.app_context():  # Ensure we're within the Flask app context
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("create table IF NOT EXISTS Student(id INT PRIMARY KEY AUTO_INCREMENT, userID varchar(255) not null unique, username varchar(255) not null, pwd varchar(255) not null, created_at Timestamp default current_timestamp, dob varchar(255), class INT not null, section char(2) not null, gender char(1) not null);")
            cursor.execute("create table IF NOT EXISTS Teacher(id INT PRIMARY KEY AUTO_INCREMENT, userID varchar(255) not null unique, username varchar(255) not null, pwd varchar(255) not null, created_at Timestamp default current_timestamp);")
            cursor.execute("create table IF NOT EXISTS Admin(id INT PRIMARY KEY AUTO_INCREMENT, userID varchar(255) not null unique, username varchar(255) not null, pwd varchar(255) not null, created_at Timestamp default current_timestamp);")
            mysql.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
def createDataTables():
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('Create Table if not Exists Test(id INT Primary Key auto_increment, dataName varchar(255) not null, dataDate varchar(255));')
            cursor.execute("CREATE TABLE IF NOT EXISTS Notice (id INT PRIMARY KEY AUTO_INCREMENT,dataName VARCHAR(255) NOT NULL, dataDate varchar(255));")
            cursor.execute('Create Table if not Exists Holidays(id INT Primary Key auto_increment, dataName varchar(255) not null, dataDate varchar(255));')
            mysql.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()


def ensure_default_entry():
    with app.app_context():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Student")
            StudentCount = cursor.fetchone()[0]
            if StudentCount == 0:
                cursor.execute("INSERT INTO Student (userID, username, pwd, dob, class, section, gender) VALUES ('student', 'student', 'student', '2005-08-15', 10, 'A', 'M');")
                mysql.connection.commit()
            cursor.execute("SELECT COUNT(*) FROM Teacher")
            TeacherCount = cursor.fetchone()[0]
            if TeacherCount == 0:
                cursor.execute("INSERT INTO Teacher (userID, username, pwd) VALUES ('teacher', 'teacher', 'teacher');")
                mysql.connection.commit()
            cursor.execute("SELECT COUNT(*) FROM Admin")
            AdminCount = cursor.fetchone()[0]
            if AdminCount == 0:
                cursor.execute("INSERT INTO Admin (userID, username, pwd) VALUES ('admin', 'admin', 'admin');")
                mysql.connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/edit_student/<int:StudentId>', methods=['GET', 'POST'])
def edit_student(StudentId):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Student WHERE id=%s', (StudentId,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return render_template('s_edit.html', user=user)
        else:
            return redirect(url_for('login'))

@app.route('/student_editing', methods=['GET', 'POST'])
def student_editing():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        try: 
            column = request.form['column']
            value = request.form[column]
            query = f'update Student set {column}=%s WHERE id=%s'
            uid = session.get('id')
            cursor.execute(query, (value, uid))
            mysql.connection.commit()
            cursor.close()
            render_template("s_edit.html")
            session.clear()  # Clear all session data
            return redirect(url_for('login'))
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()


@app.route('/teacher_editing', methods=['GET', 'POST'])
def teacher_editing():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        try:
            column = request.form['column']
            value = request.form[column]
            query = f'update Teacher set {column}=%s WHERE id=%s'
            uid = session.get('id')
            cursor.execute(query, (value, uid))
            mysql.connection.commit()
            cursor.close()
            render_template("t_edit.html")
            session.clear()
            return redirect(url_for('login'))  
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()



@app.route('/admin_editing', methods=['GET', 'POST'])
def admin_editing():
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        try:
            column = request.form['column']
            value = request.form[column]
            query = f'update Admin set {column}=%s WHERE id=%s'
            uid = session.get('id')
            cursor.execute(query, (value, uid))
            mysql.connection.commit()
            cursor.close()
            render_template("a_edit.html")
            session.clear()
            return redirect(url_for('login'))  # Clear all session data
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()




@app.route('/edit_teacher/<int:TeacherId>', methods=['GET', 'POST'])
def edit_teacher(TeacherId):
    if request.method == 'POST':
       cursor = mysql.connection.cursor()
       cursor.execute('SELECT * FROM Teacher WHERE id=%s', (TeacherId,))
       user = cursor.fetchone()
       if user:
         return render_template("t_edit.html")
       else:
           return redirect(url_for("dashboardPage"))


@app.route('/edit_admin/<int:AdminId>', methods=['GET', 'POST'])
def edit_admin(AdminId):
    if request.method == 'POST':
       cursor = mysql.connection.cursor()
       cursor.execute('SELECT * FROM Admin WHERE id=%s', (AdminId,))
       user = cursor.fetchone()
       if user:
         return render_template("a_edit.html")
       else:
           return redirect(url_for("dashboardPage"))



@app.route('/delete_holiday/<int:HolidayId>', methods=['GET', 'POST'])
def delete_holiday(HolidayId):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Holidays WHERE id = %s', (HolidayId,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('dashboardPage'))



@app.route('/delete_notice/<int:NoticeId>', methods=['GET', 'POST'])
def delete_notice(NoticeId):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Notice WHERE id = %s', (NoticeId,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('dashboardPage'))



@app.route('/delete_test/<int:TestId>', methods=['GET', 'POST'])
def delete_test(TestId):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Test WHERE id = %s', (TestId,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('dashboardPage'))

@app.route('/delete_student/<int:StudentId>', methods=['GET', 'POST'])
def delete_student(StudentId):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Student WHERE id = %s', (StudentId,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('dashboardPage'))

@app.route('/delete_teacher/<int:TeacherId>', methods=['GET', 'POST'])
def delete_teacher(TeacherId):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Teacher WHERE id = %s', (TeacherId,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('dashboardPage'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userType = request.form['user']
        userID = request.form['userId']
        pwd = request.form['pwd']


        cursor = mysql.connection.cursor()
        query = f'SELECT * FROM {userType} WHERE userID=%s AND pwd =%s'
        cursor.execute(query, (userID, pwd))
        user = cursor.fetchone()
        cursor.close()

        if user:
            if userType == 'Student':
                session['loggedin'] = True
                session['userId'] = user[1]
                session['username'] = user[2]
                session['class'] = user[6]
                session['section'] = user[7]
                session['userType'] = userType
            if userType == 'Teacher':
                session['loggedin'] = True
                session['userId'] = user[1]
                session['username'] = user[2]
                session['class'] = ""
                session['section'] = ""
                session['userType'] = userType
            if userType == 'Admin':
                session['loggedin'] = True
                session['userId'] = user[1]
                session['username'] = user[2]
                session['class'] = ""
                session['section'] = ""
                session['userType'] = userType
            session['id'] = user[0]
            return redirect(url_for("dashboardPage"))
        else:
            return "invalid login credentials"
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboardPage():
    if request.method == 'POST':
        dataType = request.form['type']
        dName = request.form['name']
        dDate = request.form['date']

        cursor = mysql.connection.cursor()
        query = f'INSERT INTO {dataType}(dataName, dataDate) VALUES(%s, %s)'
        cursor.execute(query, (dName, dDate))
        mysql.connection.commit()
        cursor.close()

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Test')
    tests = cursor.fetchall()
    cursor.execute('SELECT * FROM Notice')
    notices = cursor.fetchall()
    cursor.execute('SELECT * FROM Holidays')
    holidays = cursor.fetchall()

    cursor.execute('SELECT * FROM Student')
    students = cursor.fetchall()

    cursor.execute('SELECT * FROM Teacher')
    teachers = cursor.fetchall()

    cursor.execute('SELECT * FROM Admin')
    admins = cursor.fetchall()

    userType = session.get('userType')
    username = session.get('username')
    user_class = session.get('class')
    section = session.get('section')
    intId = session.get('id')


    cursor.close()
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        return render_template("dashboard.html", tests=tests, notices=notices, holidays=holidays, username=username, user_class=user_class, section=section, userType=userType, students=students, teachers=teachers, admins=admins, Intid=intId)

@app.route('/newAdmission', methods=['GET', 'POST'])
def newAdmission():
    if request.method == 'POST':
        userType = request.form['user']
        if userType == "Student":
            dob = request.form['dob']
            class_ = request.form['class']
            section = request.form['section']
            gender = request.form['gender']
            userID = request.form['userId']
            username = request.form['username']
            pwd = request.form['pwd']
            cursor = mysql.connection.cursor()
            query = f'INSERT INTO {userType}(userID, username, pwd, dob, class, section, gender) VALUES(%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(query, (userID, username, pwd, dob, class_, section, gender))
            mysql.connection.commit()
            cursor.close()
        else:
            pwd = request.form['pwd']
            userID = request.form['userId']
            username = request.form['username']
            cursor = mysql.connection.cursor()
            query = f'INSERT INTO {userType}(userID, username, pwd) VALUES(%s, %s, %s)'
            cursor.execute(query, (userID, username, pwd))
            mysql.connection.commit()
            cursor.close()
        return render_template('login.html')
    return render_template('newAdmission.html')


if __name__ == '__main__':
    # app.run(debug=True, host='localhost', port=500)
    create_userTables()
    createDataTables()
    ensure_default_entry()
    app.run(debug=True, port=5001)



from flask import *
from flask_mysqldb import MySQL   
from MySQLdb.cursors import DictCursor                
from dotenv import load_dotenv                    
import os                                          

load_dotenv()


app = Flask(__name__)
app.secret_key = 'abcde12345'  

app.config['MYSQL_HOST'] = os.getenv('HOST')        
app.config['MYSQL_USER'] = os.getenv('USER')          
app.config['MYSQL_PASSWORD'] = os.getenv('PASSWORD')  
app.config['MYSQL_DB'] = os.getenv('DB')             

mysql = MySQL(app)

# print(os.getenv('HOST'), os.getenv('USER'), os.getenv('PASSWORD'), os.getenv('DB'))

@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/welcome')
def welcome():
   return render_template('welcome.html')  

@app.route('/admin')
def admin():
    cur2=mysql.connection.cursor()
    cur2.execute("SELECT * FROM emp")
    data2=cur2.fetchall()
    cur2.close()
    return render_template('admin.html',user_data=data2)  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        

        if (email == "admin@gmail.com" and password=="admin123"):
            return redirect(url_for('admin'))
    
        cur = mysql.connection.cursor(cursorclass=DictCursor)
        cur.execute("SELECT * FROM emp WHERE email=%s AND password=%s", (email, password))
        data = cur.fetchone()
        cur.close()

        if data is None and email != "admin@gmail.com" and password!="admin123":
            flash("Invalid Email or Password", "danger")
            return render_template('login.html')

        else:
            session['loggedin'] = True
            session['id'] = data['id']
            session['username'] = data['username']
            session['email'] = data['email']
            return redirect(url_for('welcome'))
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        age = request.form['age']
        dept = request.form['dept']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        cur1 = mysql.connection.cursor()
        cur1.execute('SELECT email FROM emp WHERE id = %s', (id,))
        existing = cur1.fetchone()

        if existing:
            flash("User with this ID already exists.")
            return render_template('register.html')
        
        else:
            cur1.execute(
                    "INSERT INTO emp (id, username, age, dept, phone, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (id, username, age, dept, phone, email, password)
                )
            mysql.connection.commit()
            cur1.close()
            return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == "__main__":
    app.run(debug=True)
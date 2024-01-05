from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 as sql

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app = Flask(__name__,  static_folder='static')
app.static_folder = 'static'
app.secret_key = 'you secret key'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.template_folder = 'templates'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_db_connection():
    conn = sql.connect('new_database.db')
    conn.row_factory = sql.Row
    return conn

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def insert_user(username, password):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO Users (Username, PasswordHash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True 
    except Exception as e:
        print(f"Error during registration: {e}")
        return False
    finally:
        conn.close()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/")
def index():
    username = None
    if "user" in session:
        user = session["user"]
        username = user["Username"]
    return render_template("index.html", username=username)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/welcome", methods=["POST"])
def welcome():
    name = request.form["name"]
    return render_template("welcome.html", name=name)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/about")
def about():
    user = None
    if 'user' in session:
        user = session['user']
        username = user["Username"]

    return render_template("about.html", user=user)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~horror~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/horror")
def horror():
    return render_template("horror.html")

@app.route('/horror/GenreH/<path:filename>')
def serve_horror_story(filename):
    return send_from_directory('stories/GenreH', filename)

@app.route('/stories/GenreH/Hstory_easy.html')
def Hstory_easy():
    return render_template('stories/GenreH/Hstory_easy.html')

@app.route('/stories/GenreH/Hstory_medium.html')
def Hstory_medium():
    return render_template('stories/GenreH/Hstory_medium.html')

@app.route('/stories/GenreH/Hstory_hard.html')
def Hstory_hard():
    return render_template('stories/GenreH/Hstory_hard.html')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~mystery~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/mystery')
def mystery():
    return render_template("mystery.html")

@app.route('/mystery/GenreM/<path:filename>')
def serve_story(filename):
    return send_from_directory('stories/GenreM', filename)

@app.route('/stories/GenreM/Mstory_easy.html')
def Mstory_easy():
    return render_template('stories/GenreM/Mstory_easy.html')

@app.route('/stories/GenreM/Mstory_medium.html')
def Mstory_medium():
    return render_template('stories/GenreM/Mstory_medium.html')
    
    
@app.route('/stories/GenreM/Mstory_hard.html')
def Mstory_hard():
    return render_template('stories/GenreM/Mstory_hard.html')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~fantasy~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/fantasy")
def fantasy():
    return render_template("fantasy.html")

@app.route('/fantasy/GenreF/<path:filename>')
def serve_fantasy_story(filename):
    return send_from_directory('stories/GenreF', filename)

@app.route('/stories/GenreF/Fstory_easy.html')
def Fstory_easy():
    return render_template('stories/GenreF/Fstory_easy.html')

@app.route('/stories/GenreF/Fstory_medium.html')
def Fstory_medium():
    return render_template('stories/GenreF/Fstory_medium.html')
    
    
@app.route('/stories/GenreF/Fstory_hard.html')
def Fstory_hard():
    return render_template('stories/GenreF/Fstory_hard.html')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~romance~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/romance")
def romance():
    return render_template("romance.html")


@app.route('/romance/GenreR/<path:filename>')
def serve_romance_story(filename):
    return send_from_directory('stories/GenreR', filename)

@app.route('/stories/GenreR/Rstory_easy.html')
def Rstory_easy():
    return render_template('stories/GenreR/Rstory_easy.html')

@app.route('/stories/GenreR/Rstory_medium.html')
def Rstory_medium():
    return render_template('stories/GenreR/Rstory_medium.html')
    
    
@app.route('/stories/GenreR/Rstory_hard.html')
def Rstory_hard():
    return render_template('stories/GenreR/Rstory_hard.html')


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/users")
def users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template("users.html", users=users)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/login", methods=["GET", "POST"])
def login():
    category = ' '
    output = ' '
    if request.method == "POST":
        conn = get_db_connection()
        curs = conn.cursor()
        curs.execute("SELECT * FROM Users WHERE Username=?", [request.form["username"]])

        try:
            user = dict(curs.fetchone())
            if request.form["username"] == user["Username"] and check_password_hash(user["PasswordHash"], request.form["password"]):
                session["user"] = user
                conn.close()
                return redirect(url_for('index'))
            else:
                category = "danger"
                output = "Login failed!"
        except Exception as e:
            category = "danger"
            output = f"Login failed: {e}"
        conn.close()

    return render_template("login.html", category=category, output=output)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if insert_user(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        else:
            flash('Registration failed. Please try again.', 'danger')

    return render_template("register.html")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route("/profile")
def profile():
    if "user" in session:
        user = session["user"]
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('login'))
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route("/track_activity", methods=["POST"])
def track_activity():
    return redirect(url_for('profile'))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    app.run(debug=True)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


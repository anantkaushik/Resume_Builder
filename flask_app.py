
from flask import Flask, render_template, redirect, url_for, request, g, session, send_from_directory
import sqlite3 as sql,os, json

app=Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.secret_key = os.urandom(24)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        if request.form['password'] == request.form['repassword']:
            try:
                name = request.form['name']
                emailid = request.form['email']
                emailid = emailid.lower()
                password = request.form['password']
                print(name,emailid,password)
                con = sql.connect("static/resumebuilder.db")
                cur = con.cursor()
                cur.execute("select uid from credentials where email = ?",(emailid,))
                a = cur.fetchone()
                if a != None:
                    return "<h1>User Already Exist</h1>"
                cur.execute("INSERT INTO credentials (name,password,email)VALUES (?,?,?)",(name,password,emailid))
                cur.execute("select uid from credentials where email = ?",(emailid,))
                a = str(cur.fetchone())
                a = a[1:-2]
                cur.execute("INSERT INTO user (uemail,uid) VALUES (?,?)",(emailid,a))
                con.commit()
                cur.close()
                con.close()
                return redirect("/")
            except:
                cur.close()
                con.close()
                return "<h1>Something Went Wrong Try Again!</h1>"
        else:
            return "<h1>Password and Confirm password does not matched</h1>"
    return "<h1>Something Went Wrong Try Again</h1>"

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        emailid = request.form['emailLogin']
        password = request.form['passwordLogin']
        print(emailid,password)
        con = sql.connect("static/resumebuilder.db")
        cur = con.cursor()
        try:
            cur.execute("select uid from credentials where email = ?",(emailid,))
            uid = cur.fetchone()
        except:
            return "<h1>User Does Not Exist</h1>"
        emailid = emailid.lower()
        cur.execute("select password from credentials where email = ?",(emailid,))
        a = cur.fetchone()
        print(a)
        cur.execute("select name from credentials where email = ?",(emailid,))
        b = cur.fetchone()
        cur.close()
        con.close()
        uid = str(uid)
        uid = uid[1:-2]
        ta=str(a)
        output=ta[2:-3]
        tb=str(b)
        name=tb[2:-3]
        session.pop('user', None)
        if request.form['passwordLogin'] == output and output != '':
            session['user'] = name
            session['email'] = emailid
            session['uid'] = uid
            return redirect('/form')
        return "<h1>Password and EmailId does not matched</h1>"
    else:
      return render_template("index.html")

@app.route("/form")
def form():
    if 'user' in session:
        return render_template("info.html")
    return redirect("/")

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/addbasic', methods = ['GET','POST'])
def addbasic():
    name = request.form['uname']
    email = request.form['uemail']
    mob = request.form['umobno']
    objective = request.form['uobjective']
    address = request.form['uaddress'] if request.form['uaddress'] else "NULL" 
    linkedin = request.form['ulinkedin'] if request.form['ulinkedin'] else "NULL" 
    portfolio = request.form['uportfolio'] if request.form['uportfolio'] else "NULL" 
    print(session['uid'])
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("UPDATE user SET uname = ?, uemail = ?, umobno = ?, uaddress = ?, ulinkedin = ?, uportfolio = ?, uobjective = ? where uid = ?",(name,email,mob,address,linkedin,portfolio,objective,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/addPersonal', methods = ['GET','POST'])
def addPersonal():
    fname = request.form['fname'] if request.form['fname'] else "NULL"
    dob = request.form['dob'] if request.form['dob'] else "NULL"
    sex = request.form['sex'] if request.form['sex'] else "NULL"
    nationality = request.form['nationality'] if request.form['nationality'] else "NULL"
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("UPDATE user SET fname = ?, DOB = ?, sex = ?, nationality = ? where uid = ?",(fname,dob,sex,nationality,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/addAcad', methods = ['GET','POST'])
def addAcad():
    print(session['uid'])
    course = request.form['course']
    degree = request.form['degree']
    year = request.form['year']
    uniname = request.form['uniname']
    specialization = request.form['specialization']
    marksobt = request.form['marksobt']
    markstot = request.form['markstot']
    marks = request.form['marks']
    print(course,degree,year,uniname,specialization,marksobt,markstot,marks,sep='\n')
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("select uid from academics where uid = ? and degree = ?",(session['uid'],degree))
    a = cur.fetchone()
    if a != None:
        cur.execute("DELETE from academics where uid = ? and degree = ?",(session['uid'],degree))
    cur.execute("INSERT INTO academics (degree,course,year,uniname,specialization,marksobt,markstot,marks,uid)VALUES (?,?,?,?,?,?,?,?,?)",(degree,course,year,uniname,specialization,marksobt,markstot,marks,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/delAcad', methods = ['GET','POST'])
def delAcad():
    course = request.form['course']
    degree = request.form['degree']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("DELETE from academics where uid = ? and degree = ?",(session['uid'],degree))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/addWE', methods = ['GET','POST'])
def addWE():
    ename = request.form['ename']
    etype = request.form['etype']
    joindate = request.form['joindate']
    enddate = request.form['enddate']
    designation = request.form['designation']
    duties = request.form['duties']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO experience (ename,etype,joindate,enddate,designation,duties,uid)VALUES (?,?,?,?,?,?,?)",(ename,etype,joindate,enddate,designation,duties,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/delWE', methods = ['GET','POST'])
def delWE():
    ename = request.form['ename']
    etype = request.form['etype']
    joindate = request.form['joindate']
    enddate = request.form['enddate']
    designation = request.form['designation']
    duties = request.form['duties']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("DELETE from experience where uid = ? and ename = ? and etype = ? and joindate = ? and enddate = ? and designation = ? and duties = ?",(session['uid'],ename,etype,joindate,enddate,designation,duties))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/addSkills', methods = ['GET','POST'])
def addSkills():
    skills = request.form['skills']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO skills (skills,uid)VALUES (?,?)",(skills,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/delSkills', methods = ['GET','POST'])
def delSkills():
    skills = request.form['skills']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("DELETE from skills where uid = ? and skills = ?",(session['uid'],skills))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/addactivities', methods = ['GET','POST'])
def addactivities():
    activities = request.form['activities']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO activities (activities,uid)VALUES (?,?)",(activities,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/delactivities', methods = ['GET','POST'])
def delactivities():
    activities = request.form['activities']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("DELETE from activities where uid = ? and activities = ?",(session['uid'],activities))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/addachievements', methods = ['GET','POST'])
def addachievements():
    achievements = request.form['achievements']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO achievements (achievements,uid)VALUES (?,?)",(achievements,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/delachievements', methods = ['GET','POST'])
def delachievements():
    achievements = request.form['achievements']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("DELETE from achievements where uid = ? and achievements = ?",(session['uid'],achievements))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/addhobbies', methods = ['GET','POST'])
def addhobbies():
    hobbies = request.form['hobbies']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO hobbies (hobbies,uid)VALUES (?,?)",(hobbies,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/delhobbies', methods = ['GET','POST'])
def delhobbies():
    hobbies = request.form['hobbies']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("DELETE from hobbies where uid = ? and hobbies = ?",(session['uid'],hobbies))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/addref', methods = ['GET','POST'])
def addref():
    rname = request.form['rname']
    rorg = request.form['rorg'] 
    rnum = request.form['rnum']
    remail = request.form['remail']
    print(rname,rorg,rnum,remail,sep="")
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO ref (rname,rorg,rnum,remail,uid)VALUES (?,?,?,?,?)",(rname,rorg,rnum,remail,session['uid']))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route('/delref', methods = ['GET','POST'])
def delref():
    rname = request.form['rname']
    rorg = request.form['rorg'] 
    rnum = request.form['rnum']
    remail = request.form['remail']
    conn = sql.connect('static/resumebuilder.db')
    cur = conn.cursor()
    cur.execute("DELETE from ref where uid = ? and rname = ? and rorg = ? and remail=?",(session['uid'],rname,rorg,remail))
    conn.commit()
    cur.close()
    conn.close()
    return json.dumps({'status':200})

@app.route("/resume")
def resume():
    if 'user' in session:
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        con = sql.connect("static/resumebuilder.db")
        con.row_factory = dict_factory
        cur = con.cursor()
        cur.execute("select * from user where uid = ?",(session['uid'],))
        details = cur.fetchall()
        cur.execute("select * from academics where uid = ?",(session['uid'],))
        acadDetails = cur.fetchall()
        return render_template("resume.html",userDetails = details, acadDetails = acadDetails)
    return redirect("/")

if __name__=="__main__":
	app.run(debug=True,port=5000)
from flask import Flask, render_template, request
import sqlite3 as sql, json

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("info.html")

"""@app.route("/addinfo", methods = ['POST'])
def addinfo():
    fname = request.form['fname']
    lname = request.form['lname']
    con=sql.connect("static/info.db")
    cur=con.cursor()
    cur.execute("INSERT INTO user (firstName,lastName)VALUES (?,?)",(fname,lname)) 
    con.commit()
    cur.close()
    con.close()
    return ("<h1>Hello "+fname+" "+lname+"</h1>")"""

@app.route('/addbasic', methods = ['GET','POST'])
def addbasic():
    name = request.form['uname']
    email = request.form['uemail']
    mob = request.form['umobno']
    objective = request.form['uobjective']
    address = request.form['uaddress'] if request.form['uaddress'] else "NULL" 
    linkedin = request.form['ulinkedin'] if request.form['ulinkedin'] else "NULL" 
    portfolio = request.form['uportfolio'] if request.form['uportfolio'] else "NULL" 
    print(name,email,mob,objective,address,linkedin,portfolio)
    #return json.dumps({'status':200, 'edit':edit, 'movid':mov_id})
    return json.dumps({'status':200})

if __name__=="__main__":
	app.run(debug=True,port=5000)
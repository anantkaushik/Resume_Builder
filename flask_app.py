from flask import Flask, render_template, request
import sqlite3 as sql

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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

if __name__=="__main__":
	app.run(debug=True,port=8000)
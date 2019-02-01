from flask import Flask
import sqlite3 as sql

app=Flask(__name__)

@app.route("/")
def home():
    fname = "Megha"
    lname = "Mittal"
    con=sql.connect("static/info.db")
    cur=con.cursor()
    # cur.execute("INSERT INTO user (firstName,lastName)VALUES (?,?)",(fname,lname)) 
    # con.commit()
    cur.execute("select * from user")
    info = cur.fetchall()
    print(info)
    cur.close()
    con.close()
    return ("<h1>WELCOME to Resume Builder</h1>")

if __name__=="__main__":
	app.run(debug=True,port=5000)
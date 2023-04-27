from flask import Flask,render_template,request
from sqlite3 import connect

app = Flask(__name__)
db = connect("data.db",check_same_thread=False)
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS data(no int,name varchar(20))")
db.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data",methods=["POST","GET"])
def data():
    name = request.form.get("name")
    if name == "" or name == None:
        data = cur.execute("select * from data")
        return render_template("data.html",data=data)
    cur.execute(f'INSERT INTO data VALUES(1,"{name}")')
    db.commit()
    data = cur.execute("select * from data")
    return render_template("data.html",data=data)

app.run(debug=True)
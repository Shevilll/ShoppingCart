from flask import Flask,render_template,request
from sqlite3 import connect

app = Flask(__name__)
db = connect("cart.db",check_same_thread=False)
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS data(Item varchar(50),Amount int,Price float)")
db.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add",methods=["POST","GET"])
def add():
    name = request.form.get("name")
    amount = request.form.get("amount")
    price = request.form.get("price")
    cur.execute(f'INSERT INTO data VALUES(?,?,?)',(name,amount,price))
    db.commit()
    return render_template("index.html")

@app.route("/data")
def data():
    data = cur.execute("select * from data")
    return render_template("data.html",item=data.fetchall())


if __name__ == "__main__":
    app.run(debug=True)
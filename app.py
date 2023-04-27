from flask import Flask,render_template,request
from sqlite3 import connect

app = Flask(__name__)
db = connect("cart.db",check_same_thread=False)
cur = db.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS data(Item varchar(50),Amount int,Price float)")
db.commit()
cur.close()

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/create")
def create():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/add",methods=["POST","GET"])
def add():
    cur = db.cursor()
    name = request.form.get("name")
    amount = request.form.get("amount")
    price = request.form.get("price")
    cur.execute(f'INSERT INTO data VALUES(?,?,?)',(name,amount,price))
    db.commit()
    cur.close()
    return render_template("index.html")

@app.route("/data")
def data():
    cur = db.cursor()
    data = cur.execute("select * from data")
    data = data.fetchall()
    cur.close()
    return render_template("data.html",item=data)

@app.route("/remove/<item>",methods=["POST","GET"])
def remove(item):
    cur = db.cursor()
    items = item.split(",")
    print(items)
    cur.execute("DELETE FROM data WHERE item=? and amount=? and price=?",(items[0],int(items[1]),int(float(items[2]))))
    db.commit()
    cur.close()


    cur = db.cursor()
    data = cur.execute("select * from data")
    data = data.fetchall()
    cur.close()
    return render_template("data.html",item=data)



if __name__ == "__main__":
    app.run(debug=True)
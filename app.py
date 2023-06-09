from flask import Flask, render_template, request, redirect, url_for
from sqlite3 import connect, OperationalError

app = Flask(__name__)
cart = connect("cart.db", check_same_thread=False)
users = connect("users.db", check_same_thread=False)
users.cursor().execute(
    "CREATE TABLE IF NOT EXISTS users(username varchar(50),password varchar(50))")
users.commit()
logged = False


@app.route("/", methods=["POST", "GET"])
def login():
    global username, password, logged
    username = request.form.get("username")
    password = request.form.get("password")
    logged = False
    if username != None and password != None:
        ucur = users.cursor()
        ucur.execute("SELECT * FROM users")
        data = ucur.fetchall()
        for i, j in data:
            if i == username and j == password:
                logged = True
        if logged:
            return render_template("index.html")
        else:
            error = "Account not found!!"
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")


@app.route("/create", methods=["POST", "GET"])
def create():
    cusername = request.form.get("cusername")
    if cusername != None and cusername[0].isdigit():
        error = "Username must begin with text!!"
        return render_template("createaccount.html", error=error)
    cpassword = request.form.get("cpassword")
    cur = cart.cursor()
    try:
        if cusername != None and cpassword != None:
            cur.execute(
                f"CREATE TABLE {(str(cusername))+(str(cpassword))} (Item varchar(50),Amount int,Price float)")
            cart.commit()
            cur.close()
            users.cursor().execute("INSERT INTO users VALUES(?, ?)", (cusername, cpassword))
            users.commit()
            return render_template("login.html")
        return render_template("createaccount.html")
    except:
        error = "Account already exists!!"
        return render_template("createaccount.html", error=error)


@app.route("/delete", methods=["POST", "GET"])
def delete():
    dusername = request.form.get("dusername")
    dpassword = request.form.get("dpassword")
    try:
        if dusername != None and dpassword != None:
            users.cursor().execute("DELETE FROM users WHERE username=? and password=?",
                                   (str(dusername), str(dpassword)))
            users.commit()
            cart.cursor().execute(f"DROP TABLE {dusername+dpassword}")
            cart.commit()

            return redirect(url_for("login"))
        return render_template("deleteaccount.html")
    except OperationalError:
        error = "User doesn't exist"
        return render_template("deleteaccount.html", error=error)


@app.route("/home", methods=["POST", "GET"])
def home():
    if logged:
        return render_template("index.html")
    return render_template("login.html")


@app.route("/add", methods=["POST", "GET"])
def add():
    cur = cart.cursor()
    name = request.form.get("name")
    amount = request.form.get("amount")
    price = request.form.get("price")
    cur.execute(
        f'INSERT INTO {str(username)+str(password)} VALUES(?,?,?)', (name, amount, price))
    cart.commit()
    cur.close()
    return render_template("index.html")


@app.route("/data")
def data():
    if logged:
        cur = cart.cursor()
        data = cur.execute(f"select * from {str(username)+str(password)}")
        data = data.fetchall()
        cur.close()
        return render_template("data.html", item=data)
    return render_template("login.html")


@app.route("/remove/<item>", methods=["POST", "GET"])
def remove(item: str):
    if logged:
        cur = cart.cursor()
        items = item.split(",")
        print(items)
        cur.execute(f"DELETE FROM {str(username)+str(password)} WHERE item=? and amount=? and price=?",
                    (items[0], int(items[1]), int(float(items[2]))))
        cart.commit()
        cur.close()
        return redirect(url_for("data"))
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, url_for, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

engine = create_engine("mysql+pymysql://root@127.0.0.1/maratona?charset=utf8mb4")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/runners")
def index():
    with engine.connect() as conn:
        sql = text("SELECT name, lastname, email from runners")
        result = conn.execute(sql)
        runners = result.all()
    return render_template("runners.html", runners=runners)

@app.route("/runners/<int:id>")
def show(id):
    with engine.connect() as conn:
        sql = text("SELECT name, lastname, email from runners")
        result = conn.execute(sql)
        runners = result.get
    return render_template("runners.html", runners=runners)


@app.route("/iscriviti", methods=["GET"])
def subscribe():
    return render_template("form.html")


@app.route("/iscriviti", methods=["POST"])
def subscribe_confirm():
    with engine.connect() as conn:
        sql = text(
            "INSERT INTO runners (name, lastname, email) VALUES ('"
            + request.form["name"]
            + "','"
            + request.form["lastname"]
            + "','"
            + request.form["email"]
            + "');"
        )
        result = conn.execute(sql)
        conn.commit()
    return render_template("confirm.html", nome=request.form["name"])

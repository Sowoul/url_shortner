from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from string import ascii_uppercase
from random import choice


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///links.sqlite3"
db = SQLAlchemy()
db.init_app(app)


class Link(db.Model):
    short = db.Column("short", db.String(8), primary_key=True)
    link = db.Column("link", db.String(500))

    def __init__(self, short, link):
        self.short = short
        self.link = link


def gen_rand(ln):
    while True:
        temp = ""
        for _ in range(ln):
            temp += choice(ascii_uppercase)
        if db.session.query(Link.short).filter_by(short=temp).first() is None:
            return temp


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        to_shorten = request.form.get("link", "")
        if to_shorten == "":
            return render_template("index.html", error="No link provided")
        code = gen_rand(8)
        newlink = Link(code, to_shorten)
        db.session.add(newlink)
        db.session.commit()
        return render_template("index.html", message=f"localhost:8080/redir/{code}")
    return render_template("index.html")


@app.route("/redir/<toredir>")
def redir(toredir):
    final = db.session.query(Link.link).filter_by(short=toredir).first()
    return redirect(final[0])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8080, debug=True)

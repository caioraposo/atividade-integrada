TAMANHO_GOL = 7

from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from math import degrees, atan, sqrt


app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://monty:some_pass@localhost/db_1"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    club = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)


def calculate(pos):
    pos = float(pos)
    return degrees(atan(TAMANHO_GOL / (2 * sqrt(pos * TAMANHO_GOL + pos * pos))))


@app.route("/", methods=["GET", "POST"])
def index():
    players = Player.query.all()
    if request.method == "POST":
        form = request.form
        pos = form.get("playerPosition")
        if pos:
            angle = round(calculate(pos), 2)
            return render_template(
                "index.html", players=players, player=form.get("playerSelection"), angle=angle
            )
        else:
            player = Player(
                name=form.get("name"),
                club=form.get("club"),
                age=form.get("age"),
            )
            db.session.add(player)
            db.session.commit()
            return redirect("/")
    return render_template("index.html", players=players, player="", angle="")


if __name__ == "__main__":
    app.run()

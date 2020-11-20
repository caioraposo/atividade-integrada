TAMANHO_GOL = 7

from flask import Flask, render_template, request
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
    distance = db.Column(db.Integer, nullable=False)


def calculate(pos):
    pos = float(pos)
    return degrees(atan(TAMANHO_GOL / (2 * sqrt(pos * TAMANHO_GOL + pos * pos))))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = request.form
        distance = form["distance"]
        player = Player(name=form["name"], club=form["club"], age=form["age"], distance=distance)
        db.session.add(player)
        db.session.commit()
        return str(calculate(distance))
    players = Player.query.all()
    results = [
        {"name": player.name, "age": player.age, "club": player.club, "distance": player.distance}
        for player in players
    ]
    return {"count": len(results), "players": results}


if __name__ == "__main__":
    app.run()

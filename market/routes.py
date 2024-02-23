from market import app
from market import db
from flask import render_template, redirect, url_for

from market.models import Item
from market.models import User

import random


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)


@app.route("/add")
def add():
    # user = User(
    #     username="admin1", email_address="admin1@exmaple.com", password_hash="kukuriku"
    # )
    item = Item(
        name=f"Item {random.randint(1, 1000000)}",
        price=random.randint(100, 10000),
        barcode=str(random.randint(1000000, 10000000)),
        description=f"description {random.randint(1, 1000)}",
    )
    db.session.add(item)
    db.session.commit()
    return redirect(url_for("market_page"))

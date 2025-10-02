from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

# MODELS
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    funds = db.Column(db.Float, default=10000.0)

    portfolio = db.relationship("Portfolio", backref="user", lazy=True)


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    quantity = db.Column(db.Integer, default=0)

    stock = db.relationship("Stock")


# Create tables
with app.app_context():
    db.create_all()


# ROUTES
@app.route("/")
def home():
    return redirect(url_for("market"))

# MARKET
@app.route("/market")
def market():
    return render_template("market.html")

# PORTFOLIO
@app.route("/portfolio")
def portfolio():
    user = User.query.first()
    return render_template("portfolio.html", user=user)



@app.route("/funds")
def funds():
    return render_template("funds.html")

@app.route("/transactions")
def transactions():
    return render_template("transactions.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")



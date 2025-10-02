<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
=======
# ------------------------------------------------------------
# Imports
# ------------------------------------------------------------
from flask import request, redirect, url_for, flash  # (you asked to add these)
from datetime import datetime, time
from decimal import Decimal
>>>>>>> Bhuwana/initial-templates

from flask import Flask, render_template, jsonify, session  # >>> ADDED session <<<
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text, inspect
from sqlalchemy_utils import database_exists, create_database

# Password hashing
from werkzeug.security import generate_password_hash, check_password_hash  # >>> ADDED <<<

from functools import wraps  # >>> ADDED <<<


# ------------------------------------------------------------
# App & DB Config
# ------------------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret"

<<<<<<< HEAD
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
=======
DB_URI = "mysql+pymysql://root:Bpassword@localhost/Stocks"
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ------------------------------------------------------------
# Models (unchanged structure, but we will hash Password values)
# ------------------------------------------------------------
class Customer(db.Model):
    __tablename__ = "customer"
    CustomerID = db.Column(db.Integer, primary_key=True)
    FullName = db.Column(db.String(120), nullable=False)
    Username = db.Column(db.String(60), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(256), nullable=False)  # store HASH here
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    portfolios = db.relationship("Portfolio", back_populates="customer", cascade="all, delete-orphan")
    orders = db.relationship("OrderHistory", back_populates="customer", cascade="all, delete-orphan")
    transactions = db.relationship("FinancialTransactions", back_populates="customer", cascade="all, delete-orphan")


class Administrator(db.Model):
    __tablename__ = "administrator"
    AdminID = db.Column(db.Integer, primary_key=True)
    FullName = db.Column(db.String(120), nullable=False)
    Username = db.Column(db.String(60), unique=True, nullable=False)
    Password = db.Column(db.String(256), nullable=False)  # store HASH here

    markets = db.relationship("StockMarket", back_populates="admin")
    stocks_managed = db.relationship("StockInventory", back_populates="admin")


class Company(db.Model):
    __tablename__ = "company"
    CompanyID = db.Column(db.Integer, primary_key=True)
    CompanyName = db.Column(db.String(120), nullable=False)
    TickerSymbol = db.Column(db.String(16), unique=True, nullable=False)
    Description = db.Column(db.String(255))

    stocks = db.relationship("StockInventory", back_populates="company")


class StockMarket(db.Model):
    __tablename__ = "stock_market"
    MarketID = db.Column(db.Integer, primary_key=True)
    AdminID = db.Column(db.Integer, db.ForeignKey("administrator.AdminID"), nullable=False)
    MarketName = db.Column(db.String(120), nullable=False)
    OpeningTime = db.Column(db.Time, nullable=False)
    ClosingTime = db.Column(db.Time, nullable=False)
    Currency = db.Column(db.String(16), default="USD")

    admin = db.relationship("Administrator", back_populates="markets")


class StockInventory(db.Model):
    __tablename__ = "stock_inventory"
    StockID = db.Column(db.Integer, primary_key=True)
    CompanyID = db.Column(db.Integer, db.ForeignKey("company.CompanyID"), nullable=False)
    AdminID = db.Column(db.Integer, db.ForeignKey("administrator.AdminID"), nullable=False)

    StockName = db.Column(db.String(120), nullable=False)
    PriceAtPurchase = db.Column(db.Numeric(12, 2), nullable=False)
    CurrentPrice = db.Column(db.Numeric(12, 2), nullable=False)
    DailyHigh = db.Column(db.Numeric(12, 2), nullable=False)
    DailyLow = db.Column(db.Numeric(12, 2), nullable=False)
    Volume = db.Column(db.BigInteger, default=0)
    LastUpdated = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship("Company", back_populates="stocks")
    admin = db.relationship("Administrator", back_populates="stocks_managed")

    orders = db.relationship("OrderHistory", back_populates="stock")
    portfolios = db.relationship("Portfolio", back_populates="stock")


class OrderHistory(db.Model):
    __tablename__ = "order_history"
    OrderID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey("customer.CustomerID"), nullable=False)
    StockID = db.Column(db.Integer, db.ForeignKey("stock_inventory.StockID"), nullable=False)

    OrderQuantity = db.Column(db.Integer, nullable=False)
    CostAtPurchase = db.Column(db.Numeric(12, 2), nullable=False)
    Side = db.Column(db.Enum("BUY", "SELL", name="side"), nullable=False)
    Status = db.Column(db.Enum("PLACED", "CANCELLED", "FILLED", "REJECTED", name="status"),
                       nullable=False, default="PLACED")
    PlacedAt = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship("Customer", back_populates="orders")
    stock = db.relationship("StockInventory", back_populates="orders")
    transaction = db.relationship("FinancialTransactions", back_populates="order", uselist=False)


class FinancialTransactions(db.Model):
    __tablename__ = "financial_transactions"
    TransactionID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey("customer.CustomerID"), nullable=False)
    OrderID = db.Column(db.Integer, db.ForeignKey("order_history.OrderID"), nullable=True)

    TransactionType = db.Column(db.Enum("DEPOSIT", "WITHDRAW", "BUY", "SELL", name="txn_type"), nullable=False)
    Amount = db.Column(db.Numeric(12, 2), nullable=False)
    TransactionDate = db.Column(db.DateTime, default=datetime.utcnow)
    TransactionStatus = db.Column(db.String(32), default="SUCCESS")

    customer = db.relationship("Customer", back_populates="transactions")
    order = db.relationship("OrderHistory", back_populates="transaction")


class Portfolio(db.Model):
    __tablename__ = "portfolio"
    PortfolioID = db.Column(db.Integer, primary_key=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey("customer.CustomerID"), nullable=False)
    StockID = db.Column(db.Integer, db.ForeignKey("stock_inventory.StockID"), nullable=True)

    CashBalance = db.Column(db.Numeric(12, 2), default=0)
    TotalCostOfOwnership = db.Column(db.Numeric(12, 2), default=0)
    Quantity = db.Column(db.Integer, default=0)
    AvgCost = db.Column(db.Numeric(12, 2), default=0)

    customer = db.relationship("Customer", back_populates="portfolios")
    stock = db.relationship("StockInventory", back_populates="portfolios")


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def cash_balance(customer_id: int) -> Decimal:
    total = db.session.query(
        func.coalesce(func.sum(FinancialTransactions.Amount), 0)
    ).filter(FinancialTransactions.CustomerID == customer_id).scalar()
    return Decimal(total)


def login_required(f):
    """Require any logged-in user (customer or admin)."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    """Require an admin account."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return wrapper


def get_or_create_admin():
    """Returns an admin; creates a default one if none exists (with HASHED password)."""
    admin = Administrator.query.first()
    if not admin:
        admin = Administrator(
            FullName="Default Admin",
            Username="admin",
            Password=generate_password_hash("password")  # ✅ HASHED correctly
        )
        db.session.add(admin)
        db.session.flush()
    return admin


def get_or_create_company(ticker: str, company_name: str):
    company = Company.query.filter_by(TickerSymbol=ticker.upper()).first()
    if not company:
        company = Company(
            CompanyName=company_name.strip() or ticker.upper(),
            TickerSymbol=ticker.upper(),
            Description=f"{company_name.strip()} stock"
        )
        db.session.add(company)
        db.session.flush()
    return company


# ------------------------------------------------------------
# Init DB before first request
# ------------------------------------------------------------
@app.before_request
def init_db():
    if not database_exists(DB_URI):
        create_database(DB_URI)
    db.create_all()
    # ensure there's at least one admin right away
    get_or_create_admin()
    db.session.commit()



# ------------------------------------------------------------
# Auth Routes
# ------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Flow:
    1) On GET -> render login page.
    2) On POST -> try Administrator first (by Username), then Customer.
       - Compare hashes with check_password_hash.
       - Set session with role.
    """
    msg = ""
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()

        if not username or not password:
            msg = "Please enter username and password."
            return render_template("login.html", msg=msg)

        # Try admin first
        admin = Administrator.query.filter_by(Username=username).first()
        if admin and check_password_hash(admin.Password, password):
            session["user_id"] = admin.AdminID
            session["username"] = admin.Username
            session["role"] = "admin"
            flash("Logged in as Admin.", "success")
            return redirect(url_for("home"))

        # Then try customer
        cust = Customer.query.filter_by(Username=username).first()
        if cust and check_password_hash(cust.Password, password):
            session["user_id"] = cust.CustomerID
            session["username"] = cust.Username
            session["role"] = "customer"
            flash("Logged in successfully.", "success")
            return redirect(url_for("home"))

        msg = "Incorrect username/password!"

    return render_template("login.html", msg=msg)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Customer registration only.
    Stores HASHED password.
    """
    msg = ""
    if request.method == "POST":
        full_name = (request.form.get("full_name") or "").strip()
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()
        password = (request.form.get("password") or "").strip()

        # Basic validation
        if not full_name or not username or not email or not password:
            msg = "Please fill out all fields."
            return render_template("register.html", msg=msg)

        # Uniqueness checks
        if Customer.query.filter_by(Username=username).first():
            msg = "Username already exists."
            return render_template("register.html", msg=msg)
        if Customer.query.filter_by(Email=email).first():
            msg = "Email already exists."
            return render_template("register.html", msg=msg)

        # Create customer with HASHED password
        cust = Customer(
            FullName=full_name,
            Username=username,
            Email=email,
            Password=generate_password_hash(password)
        )
        db.session.add(cust)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", msg=msg)



@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ------------------------------------------------------------
# App Pages (some protected)
# ------------------------------------------------------------
@app.route("/")
def home():
    # Landing page — show base or a home screen
    return render_template("base.html")  # or render_template("home.html")


@app.route("/portfolio")
@login_required
def portfolio_page():
    # For demo/testing, use current session user if role==customer; else fallback
    cid = None
    if session.get("role") == "customer":
        cid = session.get("user_id")
    if not cid:
        # default demo user id
        cid = 1

    holdings = (
        db.session.query(Portfolio, StockInventory)
        .outerjoin(StockInventory, Portfolio.StockID == StockInventory.StockID)
        .filter(Portfolio.CustomerID == cid, Portfolio.Quantity > 0)
        .all()
    )
    rows, total_stock_value = [], Decimal("0.00")
    for p, s in holdings:
        last = Decimal(s.CurrentPrice) if s else Decimal("0")
        value = last * p.Quantity
        pl = value - (Decimal(p.AvgCost) * p.Quantity)
        rows.append({
            "ticker": (s.StockName if s else "—"),
            "qty": p.Quantity,
            "avg_cost": Decimal(p.AvgCost),
            "last": last,
            "value": value,
            "pl": pl
        })
        total_stock_value += value

    cash = cash_balance(cid)
    total_value = cash + total_stock_value
    return render_template(
        "portfolio.html",
        title="Portfolio",
        rows=rows,
        cash=cash,
        total_stock_value=total_stock_value,
        total_value=total_value
    )

>>>>>>> Bhuwana/initial-templates

# MARKET
@app.route("/market")
def market_page():
    stocks = StockInventory.query.order_by(StockInventory.StockName).all()
    return render_template("market.html", stocks=stocks, title="Stock Market")


@app.route("/market/add", methods=["POST"])
@admin_required  # >>> Only admins can add stocks <<<
def market_add_stock():
    try:
        ticker = (request.form.get("ticker") or "").upper().strip()
        company_name = (request.form.get("company_name") or "").strip()
        initial_price_str = (request.form.get("initial_price") or "0").strip()
        volume_str = (request.form.get("volume") or "0").strip()

        if not ticker or not company_name:
            flash("Ticker and Company Name are required.", "danger")
            return redirect(url_for("market_page"))

        initial_price = Decimal(initial_price_str)
        volume = int(volume_str)

        admin = get_or_create_admin()
        company = get_or_create_company(ticker, company_name)

        existing = StockInventory.query.filter_by(CompanyID=company.CompanyID).first()
        if existing:
            flash(f"Stock for {ticker} already exists.", "warning")
            return redirect(url_for("market_page"))

        stock = StockInventory(
            CompanyID=company.CompanyID,
            AdminID=admin.AdminID,
            StockName=ticker,
            PriceAtPurchase=initial_price,
            CurrentPrice=initial_price,
            DailyHigh=initial_price,
            DailyLow=initial_price,
            Volume=volume
        )
        db.session.add(stock)
        db.session.commit()
        flash(f"Created {ticker} at ${initial_price} with volume {volume}.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error creating stock: {e}", "danger")

    return redirect(url_for("market_page"))


# PORTFOLIO
@app.route("/portfolio")
def portfolio():
    user = User.query.first()
    return render_template("portfolio.html", user=user)



@app.route("/funds")
@login_required
def funds():
    return render_template("funds.html")


@app.route("/transactions")
@login_required
def transactions_page():
    txns = (
        FinancialTransactions.query
        .order_by(FinancialTransactions.TransactionDate.desc())
        .limit(50).all()
    )
    return render_template("transactions.html", txns=txns, title="Transactions")


@app.route("/profile")
@login_required
def profile_page():
    # If a customer is logged in, show their profile; else fall back to id=1
    c = None
    if session.get("role") == "customer":
        c = Customer.query.get(session.get("user_id"))
    if not c:
        c = Customer.query.get(1)
    return render_template("profile.html", customer=c, title="Profile")

<<<<<<< HEAD
@app.route("/settings")
def settings():
    return render_template("settings.html")


=======

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> Bhuwana/initial-templates

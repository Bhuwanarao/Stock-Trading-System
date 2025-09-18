from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/market")
def market():
    return render_template("market.html")

@app.route("/funds")
def funds():
    return render_template("funds.html")

@app.route("/transactions")
def transactions():
    return render_template("transactions.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)

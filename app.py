from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="bookingdb",
    user="bookinguser",
    password="strongpassword"
)
cur = conn.cursor()

# 1. Static HTML - Home Page
@app.route("/")
def index():
    return render_template("index.html")

# 2. Booking Form - POST + GET
@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        cur.execute("INSERT INTO bookings (name, address) VALUES (%s, %s)", (name, address))
        conn.commit()
        return redirect("/bookings")
    return render_template("booking.html")

# 3. Show all bookings
@app.route("/bookings")
def bookings():
    cur.execute("SELECT name, address FROM bookings")
    rows = cur.fetchall()
    return render_template("bookings.html", bookings=rows)

if __name__ == "__main__":
    app.run(debug=True)

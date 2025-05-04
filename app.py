from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="bookingdb",
    user="postgres",
    password="nakul"
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

        # Step 1: Insert user into users table
        cur.execute(
            "INSERT INTO users (name, address) VALUES (%s, %s) RETURNING id",
            (name, address)
        )
        user_id = cur.fetchone()[0]

        # Step 2: Insert booking for that user
        cur.execute("INSERT INTO bookings (user_id) VALUES (%s)", (user_id,))
        conn.commit()

        return redirect("/bookings")

    return render_template("booking.html")

# 3. Show all bookings
@app.route("/bookings")
def bookings():
    cur.execute("""
        SELECT b.id, u.name, u.address, b.booking_date, b.status
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        ORDER BY b.id DESC
    """)
    rows = cur.fetchall()
    return render_template("bookings.html", bookings=rows)

if __name__ == "__main__":
    app.run(debug=True)


import os
import mysql.connector
from mysql.connector import IntegrityError
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

db = mysql.connector.connect(
    host="student-login-db-aniketaux-db1.g.aivencloud.com",
    port=27405,
    user="avnadmin",
    password=os.environ["DB_PASSWORD"],
    database="defaultdb",
    ssl_ca="ca.pem",
    ssl_verify_cert=True
)

print("MySQL Connected Successfully!")


# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()

        query = "SELECT password FROM students WHERE email = %s"
        cursor.execute(query, (email,))

        student = cursor.fetchone()
        cursor.close()

        if student and check_password_hash(student[0], password):
            return "Login successful!"

        return "Invalid email or password!"

    return render_template("auth.html", mode="login")


# SIGNUP PAGE
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        cursor = db.cursor()

        query = "INSERT INTO students (email, password) VALUES (%s, %s)"

        try:
            cursor.execute(query, (email, hashed_password))
            db.commit()
            return "Signup successful!"

        except IntegrityError:
            return "Email already registered!"

        finally:
            cursor.close()

    return render_template("auth.html", mode="signup")


if __name__ == "__main__":
    app.run(debug=True)

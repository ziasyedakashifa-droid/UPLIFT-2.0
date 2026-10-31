import os
import re
import secrets
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

from database import (
    init_db,
    create_user,
    get_user_by_email,
    get_user_by_id,
    save_mood,
    get_moods,
    save_journal,
    create_support_request,
    get_support_requests
)

from gemma import analyse_journal
from safety import urgent_support_message

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

init_db()


# LOGIN PROTECTION

def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.")
            return redirect(url_for("login"))

        return route_function(*args, **kwargs)

    return wrapper


def current_user():
    user_id = session.get("user_id")

    if not user_id:
        return None

    return get_user_by_id(user_id)


# HOMEPAGE

@app.route("/")
def home():
    return render_template("index.html")


# SIGNUP

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            flash("Please fill in all the fields.")
            return render_template("signup.html")

        if len(name) > 100:
            flash("Name must be under 100 characters.")
            return render_template("signup.html")

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("Please enter a valid email address.")
            return render_template("signup.html")

        if len(email) > 254:
            flash("Email address is too long.")
            return render_template("signup.html")

        if len(password) < 8 or len(password) > 128:
            flash("Password must contain 8 to 128 characters.")
            return render_template("signup.html")

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("signup.html")

        if get_user_by_email(email):
            flash("An account with this email already exists.")
            return render_template("signup.html")

        password_hash = generate_password_hash(password)

        try:
            create_user(name, email, password_hash)
        except Exception:
            app.logger.exception("Signup error")
            flash("Could not create your account. Please try again.")
            return render_template("signup.html")

        user = get_user_by_email(email)

        session.clear()
        session["user_id"] = user["id"]

        flash("Your UPLIFT account has been created successfully!")
        return redirect(url_for("dashboard"))

    return render_template("signup.html")


# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("user_id"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = get_user_by_email(email)

        if user and check_password_hash(user["password_hash"], password):

            session.clear()
            session["user_id"] = user["id"]

            flash("Welcome back, " + user["name"] + "!")
            return redirect(url_for("dashboard"))

        flash("Incorrect email address or password.")

    return render_template("login.html")


# LOGOUT

@app.route("/logout")
@login_required
def logout():

    session.clear()
    flash("You have been logged out successfully.")

    return redirect(url_for("home"))


# DASHBOARD

@app.route("/dashboard")
@login_required
def dashboard():

    user = current_user()

    if not user:
        session.clear()
        return redirect(url_for("login"))

    moods = get_moods(user["id"])

    return render_template(
        "dashboard.html",
        moods=moods,
        user=user
    )


# MOOD TRACKER

@app.route("/mood", methods=["POST"])
@login_required
def mood():

    user = current_user()

    try:
        score = int(request.form.get("score", "3"))

        if score not in range(1, 6):
            raise ValueError()

        save_mood(user["id"], score)
        flash("Mood check-in saved.")

    except ValueError:
        flash("Choose a mood from 1 to 5.")

    return redirect(url_for("dashboard"))


# MINDMIRROR JOURNAL WITH GEMMA

@app.route("/journal", methods=["GET", "POST"])
@login_required
def journal():

    user = current_user()
    result = None
    urgent = False

    if request.method == "POST":

        entry = request.form.get("journal", "").strip()

        if not entry:
            flash("Please write a reflection first.")

        elif len(entry) > 5000:
            flash("Please keep entries under 5,000 characters.")

        else:

            message = urgent_support_message(entry)

            if message:
                urgent = True

                result = {
                    "emotions": [],
                    "stressors": [],
                    "support_message": message,
                    "suggestion": "Contact a trusted person or qualified professional now.",
                    "support_option": "Human support"
                }

            else:
                try:
                    result = analyse_journal(entry)

                except Exception:
                    app.logger.exception("Gemma API error")
                    flash("AI service unavailable. Please check the Ollama connection.")

            if result:
                save_journal(
                    user["id"],
                    entry,
                    result.get("emotions", []),
                    result.get("stressors", [])
                )

    return render_template(
        "journal.html",
        result=result,
        urgent=urgent
    )


# HUMANCONNECT SUPPORT

@app.route("/support", methods=["GET", "POST"])
@login_required
def support():

    user = current_user()

    if request.method == "POST":

        concern = request.form.get("concern", "").strip()[:500]
        contact = request.form.get("contact", "").strip()[:150]

        if concern:

            create_support_request(
                user["id"],
                concern,
                contact
            )

            flash("Demo request recorded locally.")
            return redirect(url_for("support"))

        flash("Please describe the support you are requesting.")

    return render_template("support.html")


# COUNSELLOR DEMO

@app.route("/counsellor")
@login_required
def counsellor():

    counsellor_emails = {
        email.strip().lower()
        for email in os.getenv("COUNSELLOR_EMAILS", "").split(",")
        if email.strip()
    }

    user = current_user()

    if not user or user["email"].lower() not in counsellor_emails:
        abort(403)

    return render_template(
        "counsellor.html",
        requests=get_support_requests()
    )


# RUN APPLICATION

if __name__ == "__main__":
    app.run(debug=True)
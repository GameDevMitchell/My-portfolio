from flask import Flask, render_template, request, send_from_directory
from email.message import EmailMessage
import smtplib
import os


def send_email(user_info):
    my_email = os.environ.get("sender")
    password = os.environ.get("data")
    recipient = os.environ.get("recipient")

    msg = EmailMessage()
    msg["Subject"] = (
        f'Mail from {user_info["name"]} who accessed your portfolio recently'
    )
    msg["From"] = my_email
    msg["To"] = recipient
    body = (
        f"Name: {user_info['name']}\nEmail: {user_info['email']}\nPhone: {user_info['phone']}\nMessage: "
        f"{user_info['message']}"
    )
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.send_message(msg)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")


@app.route("/")
def welcome():
    return render_template("index-svg.html")


@app.route("/download CV")
def download():
    return send_from_directory("static", path="files/cheat_sheet.pdf")


@app.route("/contact", methods=["GET", "POST"])
def get_contact():
    if request.method == "POST":
        user_info = {
            "name": request.form.get("Name"),
            "email": request.form.get("E-mail"),
            "phone": request.form.get("Phone"),
            "message": request.form.get("Message"),
        }
        send_email(user_info)
        return render_template("contact.html")
    return render_template("index-svg.html")


if __name__ == "__main__":
    app.run(debug=False, port=5002)

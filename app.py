from flask import Flask, render_template, request, redirect, url_for, flash
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os
import random

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # No quotes needed here
# Routes
@app.route("/")
@app.route("/home")
def home():
    trending = [
        {'name': "Green Shyne's Angelo", 'image': 'pro5.jpg'},
        {'name': "Black Cactus", 'image': 'pro6.png'},
        {'name': "3D SOL", 'image': 'pro4.jpg'},
        {'name': "Jaadu", 'image': 'pro3.jpg'},
        {'name': "Neem Cleaner", 'image': 'pro10.jpg'},
        {'name': "Green Shyne's Power", 'image': 'pro2.jpg'},
        {'name': "Rose Hygiene", 'image': 'pro7.jpg'},
        {'name': "Lemon Drop", 'image': 'pro8.jpg'},
        {'name': "Bleach Extra", 'image': 'pro1.jpg'},
        {'name': "Sanitizer Pro", 'image': 'pro9.jpg'}
    ]
    exclusive = {
        'new': trending,
        'special': random.sample(trending, min(9, len(trending))),
        'best': random.sample(trending, min(9, len(trending)))
    }
    return render_template("home.html", trending=trending, exclusive=exclusive)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        email_content = Mail(
            from_email=os.getenv('MAIL_DEFAULT_FROM'),
            to_emails=os.getenv('MAIL_DEFAULT_TO'),
            subject="New Contact Message from Phenyle Website",
            plain_text_content=f"Name: {name}\nEmail: {email}\nMessage: {message}"
        )

        try:
            sg = SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))
            sg.send(email_content)
            return redirect(url_for("success"))
        except Exception as e:
            print(f"Email failed to send: {e}")
            flash("Failed to send your message. Please try again later.", "danger")
            return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/branch")
def branch():
    return render_template("branch.html", title="Branch")

@app.route("/media")
def media():
    return render_template("media.html", title="Media")

@app.route("/search")
def search():
    query = request.args.get('query', '').strip().lower()
    category_info = {
        "bleaching powder": "Effective for disinfection and stain removal.",
        "floor cleaner": "Keeps floors spotless and germ-free.",
        "handwash": "Gentle yet powerful on germs.",
        "mosquito repellant": "Protects against mosquito-borne diseases.",
        "napthalene": "Removes odors and repels insects in wardrobes.",
        "phenyl": "Powerful disinfectant for floors and bathrooms."
    }
    result = category_info.get(query)
    if not result:
        for key, value in category_info.items():
            if query in key:
                result = value
                break
    return render_template("search_results.html", query=query, result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

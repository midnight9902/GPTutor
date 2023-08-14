from flask import Flask, render_template, request, flash
from GPTutor import Docs
import os

os.environ.get('OPENAI_API_KEY')

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

my_docs = [
    r"pdf/Lecture-1-Summer2023.pdf",
    r"pdf/Lecture-2-Summer2023.pdf",
    r"pdf/Lecture-3-Summer2023.pdf",
    r"pdf/Lecture-4-Summer2023.pdf",
    r"pdf/Lecture-5-Summer2023.pdf",
    r"pdf/Lecture-6-Summer2023.pdf",
    r"pdf/Lecture-7-Summer2023.pdf",
    r"pdf/Lecture-8-Spring2023.pdf",
    r"pdf/Lecture-9-Spring2023.pdf"]
docs = Docs()
for d in my_docs:
    docs.add(d)

@app.route("/hello")
def index():
	flash(" ")
	return render_template("index.html")

@app.route('/greet', methods=['POST'])
def greet():
    user_query = request.form['name_input']
    answer = docs.query(user_query)
    return render_template("index.html", answer=answer.formatted_answer)

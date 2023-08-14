from flask import Flask, render_template, request, flash
from paperqa import Docs
import os
import data_handler.py

os.environ['OPENAI_API_KEY'] = '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'

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

my_docs = [
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-7-Summer2023.pdf",
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-8-Spring2023.pdf",
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-9-Spring2023.pdf",
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-1-Summer2023.pdf",
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-2-Summer2023.pdf",
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-3-Summer2023.pdf",
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-4-Summer2023.pdf",
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-5-Summer2023.pdf",
    r"C:\Eric\School\Advanced Topics in Data Science\Lecture-6-Summer2023.pdf"]
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

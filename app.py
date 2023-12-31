from flask import Flask, render_template, request, flash
from paperqa import Docs
import os
from data_handler import generate_course_data

os.environ['OPENAI_API_KEY'] = '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'

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

my_docs = generate_course_data()
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

from flask import Flask, render_template, request, flash
from GPTutor import Docs
import os

os.environ.get('OPENAI_API_KEY')

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

my_docs = generatedcoursedata
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

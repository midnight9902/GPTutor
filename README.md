This project is difficult to quantitatively measure due to the small training size and ambiguous definition of what is "in context".
To solve this we looked at the sources that it outputted and checked the pdf files for whether or not the referenced lecture and page number were indeed relevant
to the question posed.
Of the 50 questions we asked, roughly 5 from each lecture, it returned 46 correct citations for a success rate of 92%
The 4 results that were not helpful to continued learning occured when the model pulled words from slides that were primarily dominated by images


captioning info goes here


To run on your personal computer:

update the pdf file paths in the generatedcoursedata function to your local filepaths

open the anaconda prompt terminal

create a virtual environment with "conda activate venv"

navigate to where the sayHello folder is stored with "cd (filepath)"

install flask with "pip install flask"

run the command "set OPENAI_API_KEY=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"

run the command "flask run"

go to your browser and navigate to "http://127.0.0.1:5000/hello"

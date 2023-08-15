This project is difficult to quantitatively measure due to the small training size and ambiguous definition of what is "in context".
To solve this we looked at the sources that it outputted and checked the pdf files for whether or not the referenced lecture and page number were indeed relevant
to the question posed.
Of the 50 questions we asked, roughly 5 from each lecture, it returned 46 correct citations for a success rate of 92%
The 4 results that were not helpful to continued learning occured when the model pulled words from slides that were primarily dominated by images


Image Extraction, Summary Generator:
For extracting the images from the PDF and text files, PyMuPDF, Pillow, and Fitz libraries were used. Once the images were extracted and seperated into directories based on the file it was extracted from, the images were sent individually to generate summaries so that they could be sent to PaperQA model. Unfortuantely, GPT-4's multimodal input functionality is not available to most developers; therefore, this project could not utilize OpenAI's API to generate image summaries. Instead, GPTutor uses SaleForce's BLIP Pretrained model and Tesseract OCR model to generate image captions. Once the images are passed those two models, the captions are cleaned up using the NLTK and re libraries. The image summaries are saved in text files and sent to PaperQA's model for a final output to the student.


To run on your personal computer:

1. update the pdf file paths in the generatedcoursedata function to your local filepaths

2. open the anaconda prompt terminal

3. create a virtual environment with "conda activate venv"

4. navigate to where the sayHello folder is stored with "cd (filepath)"

5. install flask with "pip install flask"

6. run the command "set OPENAI_API_KEY="Insert your OpenAI API Key Here"

7. run the command "flask run"

go to your browser and navigate to "http://127.0.0.1:5000/hello"

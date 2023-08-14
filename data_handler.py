import fitz
import os
from paperqa import Docs
from PIL import Image
from transformers import pipeline
import pytesseract
import re
import nltk
from nltk.corpus import words

nltk.download('words')


# Load documents
def load_documents(course_data):
    my_docs = course_data
    docs = Docs()
    for d in my_docs:
        docs.add(d)
    return docs


def tutor_query(query, docs):
    answer = docs.query(query, k=5, max_sources=2)
    print("Answer: ", answer.formatted_answer)


def extract_images(my_docs):
    # Extract images from the given PDF documents
    file_paths = my_docs
    image_paths = []
    # print(file_paths)
    # Open pdf file using file module
    for file in file_paths:
        file_name = file[:-4]
        # find the index of the dash before the file name
        ind = 0
        for i in range(len(file_name) - 1, -1, -1):
            if file_name[i] == '/':
                ind = i
                break
        file_name = file_name[ind + 1:]
        lecture_pdf = fitz.open(file)

        # create a directory for the images in the file to get stored
        curr_dir = os.getcwd()
        new_dir = rf'/data/{file_name}/images'
        images_path = os.path.join(curr_dir, new_dir)
        # print(images_path)
        # print()
        image_paths.append(images_path)
        os.makedirs(images_path)

        # calculate the number of pages in the PDF file
        page_nums = len(lecture_pdf)

        # create empty list to store images information
        images_lst = []

        # extract image information from each page
        for page in range(page_nums):
            page_content = lecture_pdf[page]
            page_imgs = page_content.get_images()
            if len(page_imgs) != 0:
                images_lst.append((page_imgs, page))  # stores the image and its page number in the pdf

        # Raise error if PDF file has no images
        if len(images_lst) == 0:
            raise ValueError("No images found in {file}")

        # Extract and save the images
        for i, image_info in enumerate(images_lst, start=1):
            # extract the image object number
            xref = image_info[0][0][0]
            # Extract the image using the xref number
            # print(lecture_pdf)
            base_image = lecture_pdf.extract_image(xref)
            # Store the image bytes
            image_bytes = base_image['image']
            # Store the image extension
            image_ext = base_image['ext']
            # Generate the image file name
            image_fil_name = file_name + "_pg_" + str(image_info[1]) + '.' + image_ext
            # print(image_fil_name)
            # print()
            # Save the image
            with open(os.path.join(images_path, image_fil_name), 'wb') as image_file:
                image_file.write(image_bytes)
                image_file.close()
    return image_paths


def extract_english_words(strings):
    # Convert the words corpus to a set for faster lookup
    word_set = set(words.words())

    result = []

    for s in strings:
        for word in s.split():
            # Check if the word is in the words corpus and is not a title (a heuristic to exclude proper names)
            if word.lower() in word_set and not word.istitle():
                result.append(word)

    return result


def generate_img_summaries(image_paths, captioner, my_config):
    # Create a dictionary that will store all of the image captions
    img_captions = {}

    # Traverse through each file's saved images and generate captions for them
    for path in image_paths:
        img_files_lst = os.listdir(path)
        print("Path: ", path)
        print("Image_file_list: ", img_files_lst)
        print()
        for img in img_files_lst:
            print("img: ", img)
            img_path = os.path.join(path, img)
            print("image_path: ", img_path)
            # Generate the first half of the caption from the transformer model
            first_half = captioner(img_path)[0]['generated_text']
            # "C:\data\Lecture-1-Summer2023\images\Lecture-1-Summer2023_pg_19.jpeg"
            # Generate the second half of the caption from the Tesseract OCR model
            img_text = pytesseract.image_to_string(Image.open(img_path), config=my_config)

            # Clean up the text obtained from the OCR model using re and nltk libraries
            img_text = re.sub('\n', ' ', img_text)
            img_text_lst = img_text.split(' ')
            second_half = extract_english_words(img_text_lst)

            # Combine the captions generated from both models to create a caption for the image
            combined_caption = ""
            for extracted_word in second_half:
                combined_caption += extracted_word + " "
            combined_caption += first_half

            # Add the image file name, so the model knows where the information was pulled from
            final_caption = combined_caption + " - " + img
            print(final_caption)
            img_captions[img] = final_caption

    return img_captions


def convert_captions2txt(img_captions):  # input: dictionary
    img_data = []
    for img_path in img_captions.keys():
        caption = img_captions[img_path]
        safe_filename = ''.join([char if char.isalnum() else '_' for char in caption])
        img_data.append(safe_filename)
        with open(f"{safe_filename}.txt", "w") as f:
            f.write(caption)

    return img_data


def generate_course_data():
    # Setup for the image caption generators
    # Load the Pretrained Salesforce BLIP Image captioning transformer model
    captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

    # Set up Tesseract OCR config
    my_config = r'--psm 11 --oem 3'
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    query = "What does it mean if a model is overfitting?"
    os.environ['OPENAI_API_KEY'] = 'sk-qPAJXXO0GxyPButPa9b1T3BlbkFJbHXoxb7vrgf5P2HxRRn'

    # course_docs = [r'data/lecture_slides/Lecture-1-Summer2023.pdf', r'data/lecture_slides/Lecture-2-Summer2023.pdf',
    #                r'data/lecture_slides/Lecture-3-Summer2023.pdf', r'data/lecture_slides/Lecture-4-Summer2023.pdf',
    #                r'data/lecture_slides/Lecture-5-Summer2023.pdf', r'data/lecture_slides/Lecture-6-Summer2023.pdf',
    #                r'data/lecture_slides/Lecture-7-Summer2023.pdf', r'data/lecture_slides/Lecture-8-Spring2023.pdf',
    #                r'data/lecture_slides/Lecture-9-Spring2023.pdf', r'data/lecture_slides/Lecture-10-Spring2023.pdf',
    #                r'data/lecture_slides/Lecture-11-Spring2023.pdf']
    course_docs = [r'data/lecture_slides/Lecture-4-Summer2023.pdf']
    image_paths = extract_images(course_docs)
    # print(image_paths)
    img_captions = generate_img_summaries(image_paths, captioner, my_config)
    print(img_captions)
    img_data = convert_captions2txt(img_captions)
    course_data = course_docs + img_data
    # docs = load_documents(course_data)

    # tutor_query(query, docs)

    return course_data

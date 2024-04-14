import os
import json
import traceback
import PyPDF2


def read_file(file):
    text = ""
    if (file.name.endswith(".pdf")):
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page in pdf_reader.pages:
            text +=page.extract_text()
    elif (file.name.endswith(".txt")):
        with open(file,'r') as f:
            text = f.read().decode("utf-8")
    else:
        raise Exception("Unsupported file type")
    
    return text

def get_table_data(quiz_text: str):
    quiz = json.loads(quiz_text)
    quiz_table_data = []
    for key, value in quiz.items():
        mcq = value["mcq"]
        options = " | ".join(
            [
                f"{option}: {option_value}"
                for option, option_value in value["options"].items()
                ]
            )
        correct = value["correct"]
        quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})
    return quiz_table_data
import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

with open("Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)


st.title("langchain app")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("upload txt or pdf")

    mcq_count = st.number_input("number of questions",  min_value=3,  max_value=20)

    subject = st.text_input("subject", max_chars=20)

    tone = st.text_input("tone", max_chars=20, placeholder="simple")

    button = st.form_submit_button("Create")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = uploaded_file.read()
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "tone": tone,
                            "subject": subject,
                            "number": mcq_count,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                    
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

            else:
                print(cb)
                if isinstance(response,dict):
                    quiz = response.get("quiz")
                    if (quiz is not None):
                        table_data = get_table_data(quiz)
                        if (table_data is not None):
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label = "Review", value = response["review"])
                        else:
                            st.error("Error building table")
                    else:
                        st.write(response)


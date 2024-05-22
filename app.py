import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
import streamlit as st
from langchain.callbacks import get_openai_callback



with open('Response.json','r') as file:
    RESPONSE_JSON=json.load(file)
    
    
#title
st.title("MCQ Generator with Langchain")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Upload a PDF or Text file")
    
    #Input Fields
    mcq_count=st.number_input("Number of MCQs", min_value=1, max_value=25)
    subject=st.text_input("Subject",max_chars=20)
    tone=st.text_input("Comlexity Level of Questions",max_chars=20,placeholder="Easy, Medium, Hard")
    
    button=st.form_submit_button("Generate MCQs")
    
    
    if button and uploaded_file is not None and mcq_count and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text=read_file(uploaded_file)
                
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {
                        "text": text, 
                        "number": mcq_count, 
                        "subject": subject,
                        "tone": tone, 
                        "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error generating MCQs")
                
            else:                
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response, dict):
                    quiz=response.get("quiz",None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data  is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label="Review", value=response['review'])
                          
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)
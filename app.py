import json
import PyPDF2
import os
from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import re
import streamlit as st

load_dotenv(find_dotenv())

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup.get_text()

def parse_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_info(text):
    template = """
    I have a document with RFP details. Please extract the following structured information from the text:

    - Bid Number
    - Title
    - Due Date
    - Bid Submission Type
    - Term of Bid
    - Pre Bid Meeting
    - Installation
    - Bid Bond Requirement
    - Delivery Date
    - Payment Terms
    - Any Additional Documentation Required
    - MFG for Registration
    - Contract or Cooperative to use
    - Model_no
    - Part_no
    - Product
    - Contact Info
    - Company Name
    - Bid Summary
    - Product Specification

    Document text:
    {text}

    Please return the extracted information as a JSON object with the following structure:
    {{

        "Bid Number": "value",
        "Title": "value",
        "Due Date": "value",
        "Bid Submission Type": "value",
        "Term of Bid": "value",
        "Pre Bid Meeting": "value",
        "Installation": "value",
        "Bid Bond Requirement": "value",
        "Delivery Date": "value",
        "Payment Terms": "value",
        "Any Additional Documentation Required": "value",
        "MFG for Registration": "value",
        "Contract or Cooperative to use": "value",
        "Model_no": "value",
        "Part_no": "value",
        "Product": "value",
        "Contact Info": "value",
        "Company Name": "value",
        "Bid Summary": "value",
        "Product Specification": "value"
    }}
    """

    prompt = PromptTemplate(template=template, input_variables=["text"])
    formatted_prompt = prompt.format(text=text)
    response = llm.invoke(formatted_prompt)

    if hasattr(response, 'content'):
        result_text = response.content.strip()
    else:
        result_text = response.strip()

    try:
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
            return json.loads(json_text)
        else:
            st.error("No valid JSON found in the response.")
            return {}
    except json.JSONDecodeError:
        st.error("Error parsing the response as JSON.")
        return {}

def generate_json(extracted_data):
    return json.dumps(extracted_data, indent=4)

def process_rfp_document(file_path):
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'html':
        text = parse_html(file_path)
    elif file_extension == 'pdf':
        text = parse_pdf(file_path)
    else:
        st.error("Unsupported file type. Please provide an HTML or PDF file.")
        return None

    structured_data = extract_info(text)
    return structured_data

st.title("RFP Document Processor")
st.subheader("Upload an HTML or PDF document to extract structured RFP information.")

uploaded_file = st.file_uploader("Choose an HTML or PDF file", type=["html", "pdf"])

if uploaded_file:
    file_path = uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write(f"Processing file: `{file_path}`")
    data = process_rfp_document(file_path)
    if data:
        # st.json(data)
        json_output = generate_json(data)
        st.write("### Extracted JSON Data:")
        st.json(data)
        st.download_button(
            label="Download JSON",
            data=json_output,
            file_name="extracted_rfp_data.json",
            mime="application/json"
        )

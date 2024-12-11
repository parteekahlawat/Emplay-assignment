# RFP Document Processor

A Python-based tool that extracts structured information from RFP (Request for Proposal) documents in HTML or PDF format. This tool uses Google Gemini (via LangChain) for intelligent text processing and provides a Streamlit-based interface for ease of use.

## Features

- Supports HTML and PDF document parsing.
- Extracts structured data like Bid Number, Title, Due Date, and more.
- Displays extracted JSON data directly on the app interface.
- Allows users to download the extracted data as a JSON file.
- Simple and intuitive web-based interface using Streamlit.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- `pip` (Python package installer)

## Installation

Unzip this file and open the file in VS code

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

### OR 
```bash
git clone https://github.com/parteekahlawat/Emplay-assignment.git
cd Emplay-assignment
pip install -r requirements.txt
```
Note: Add a .env file and add a GOOGLE_API_KEY in .env
```bash
python -m streamlit run app.py
```


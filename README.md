# Survey-Scripting-Tool

Convert .docx Questionnaire into surveyCTO ready scripting file.

## Overview

This FastAPI-based tool provides a two-step conversion process:
1. **DOCX to JSON**: Upload a .docx questionnaire file and convert it to JSON format
2. **JSON to Excel**: Convert the JSON file to a surveyCTO-ready Excel format

## Features

- RESTful API built with FastAPI
- Interactive Swagger UI documentation
- Two-step conversion workflow:
  - Upload .docx questionnaire → Download JSON
  - Upload JSON → Download surveyCTO Excel

## Installation

1. Clone the repository:
```bash
git clone https://github.com/VikasKori12/Survey-Scripting-Tool.git
cd Survey-Scripting-Tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

2. Access the Swagger UI:
```
http://localhost:8000/docs
```

3. Use the API:
   - **Step 1**: Upload your .docx questionnaire to `/api/convert/docx-to-json`
   - Download the generated JSON file
   - **Step 2**: Upload the JSON file to `/api/convert/json-to-excel`
   - Download the surveyCTO-ready Excel file

## API Endpoints

### Root
- `GET /` - API information and available endpoints

### DOCX to JSON Conversion
- `POST /api/convert/docx-to-json` - Convert .docx to JSON
- `GET /api/download/json/{filename}` - Download generated JSON

### JSON to Excel Conversion
- `POST /api/convert/json-to-excel` - Convert JSON to Excel
- `GET /api/download/excel/{filename}` - Download generated Excel

## DOCX Format Guidelines

Your .docx questionnaire should follow this format:

```
1. What is your name?

2. What is your age?

3. Select your gender:
a) Male
b) Female
c) Other

4. Which of the following do you use? (Select all that apply)
a) Smartphone
b) Tablet
c) Laptop
d) Desktop
```

## Output Format

The tool generates an Excel file with two sheets:
- **survey**: Contains question definitions (type, name, label, required, etc.)
- **choices**: Contains choice lists for select_one and select_multiple questions

## Technologies Used

- FastAPI - Web framework
- python-docx - DOCX file parsing
- openpyxl - Excel file generation
- Uvicorn - ASGI server

## License

MIT

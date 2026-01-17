# API Testing Examples

This document provides examples of how to test the Survey Scripting Tool API using curl.

## Prerequisites

Make sure the server is running:
```bash
python main.py
# or
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint

Check if the API is running:

```bash
curl http://localhost:8000/
```

**Response:**
```json
{
    "message": "Welcome to Survey Scripting Tool API",
    "endpoints": {
        "docx_to_json": "/api/convert/docx-to-json",
        "json_to_excel": "/api/convert/json-to-excel",
        "docs": "/docs"
    }
}
```

### 2. Convert DOCX to JSON

Upload a .docx questionnaire file to convert it to JSON:

```bash
curl -X POST http://localhost:8000/api/convert/docx-to-json \
  -F "file=@/path/to/your/questionnaire.docx"
```

**Response:**
```json
{
    "status": "success",
    "message": "DOCX file converted to JSON successfully",
    "json_data": {
        "survey_name": "Questionnaire",
        "version": "1.0",
        "questions": [
            {
                "id": "q1",
                "question": "What is your full name?",
                "type": "text",
                "required": true
            }
        ]
    },
    "download_filename": "20260117_170217_questionnaire.json",
    "download_url": "/api/download/json/20260117_170217_questionnaire.json"
}
```

### 3. Download JSON File

Download the generated JSON file:

```bash
curl -o questionnaire.json \
  http://localhost:8000/api/download/json/20260117_170217_questionnaire.json
```

### 4. Convert JSON to Excel

Upload the JSON file to convert it to surveyCTO-ready Excel:

```bash
curl -X POST http://localhost:8000/api/convert/json-to-excel \
  -F "file=@questionnaire.json"
```

**Response:**
```json
{
    "status": "success",
    "message": "JSON file converted to Excel successfully",
    "download_filename": "20260117_170228_surveyCTO.xlsx",
    "download_url": "/api/download/excel/20260117_170228_surveyCTO.xlsx"
}
```

### 5. Download Excel File

Download the generated Excel file:

```bash
curl -o surveyCTO.xlsx \
  http://localhost:8000/api/download/excel/20260117_170228_surveyCTO.xlsx
```

## Complete Workflow Example

Here's a complete example of the two-step conversion process:

```bash
# Step 1: Convert DOCX to JSON
curl -X POST http://localhost:8000/api/convert/docx-to-json \
  -F "file=@sample_questionnaire.docx" \
  -o docx_response.json

# Extract the JSON filename from response (using jq)
JSON_FILE=$(cat docx_response.json | jq -r '.download_filename')

# Download the JSON file
curl -o questionnaire.json \
  "http://localhost:8000/api/download/json/$JSON_FILE"

# Step 2: Convert JSON to Excel
curl -X POST http://localhost:8000/api/convert/json-to-excel \
  -F "file=@questionnaire.json" \
  -o excel_response.json

# Extract the Excel filename from response
EXCEL_FILE=$(cat excel_response.json | jq -r '.download_filename')

# Download the Excel file
curl -o surveyCTO.xlsx \
  "http://localhost:8000/api/download/excel/$EXCEL_FILE"

echo "Conversion complete! Check surveyCTO.xlsx"
```

## Interactive API Documentation

FastAPI provides interactive API documentation. Access it at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Note: If you're behind a firewall that blocks CDN resources, the Swagger UI may not load properly. In that case, use the curl examples above or the ReDoc interface.

## Testing with Python

You can also test the API using Python's `requests` library:

```python
import requests

# Convert DOCX to JSON
with open('questionnaire.docx', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/convert/docx-to-json',
        files={'file': f}
    )
    result = response.json()
    print(f"JSON created: {result['download_filename']}")

# Download JSON
json_url = f"http://localhost:8000{result['download_url']}"
json_response = requests.get(json_url)
with open('questionnaire.json', 'wb') as f:
    f.write(json_response.content)

# Convert JSON to Excel
with open('questionnaire.json', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/convert/json-to-excel',
        files={'file': f}
    )
    result = response.json()
    print(f"Excel created: {result['download_filename']}")

# Download Excel
excel_url = f"http://localhost:8000{result['download_url']}"
excel_response = requests.get(excel_url)
with open('surveyCTO.xlsx', 'wb') as f:
    f.write(excel_response.content)

print("Conversion complete!")
```

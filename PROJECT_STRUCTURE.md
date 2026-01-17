# Survey Scripting Tool - Project Structure

## Directory Structure

```
Survey-Scripting-Tool/
├── main.py                      # FastAPI application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation
├── API_EXAMPLES.md             # API usage examples
├── .gitignore                  # Git ignore rules
│
├── routers/                    # API route handlers
│   ├── __init__.py
│   ├── docx_router.py          # DOCX to JSON endpoints
│   └── excel_router.py         # JSON to Excel endpoints
│
└── utils/                      # Utility modules
    ├── __init__.py
    ├── docx_parser.py          # DOCX parsing logic
    └── json_to_excel_converter.py  # Excel generation logic
```

## Components

### Main Application (main.py)
- FastAPI app initialization
- CORS configuration
- Router registration
- Root endpoint

### DOCX Router (routers/docx_router.py)
**Endpoints:**
- `POST /api/convert/docx-to-json` - Upload and convert DOCX file
- `GET /api/download/json/{filename}` - Download generated JSON

**Features:**
- File validation (DOCX only)
- Temporary file management
- Error handling with proper HTTP status codes

### Excel Router (routers/excel_router.py)
**Endpoints:**
- `POST /api/convert/json-to-excel` - Upload and convert JSON file
- `GET /api/download/excel/{filename}` - Download generated Excel

**Features:**
- File validation (JSON only)
- JSON parsing with error handling
- Excel file generation

### DOCX Parser (utils/docx_parser.py)
**Functionality:**
- Parses numbered questions (1., 2., Q1., etc.)
- Detects choice options (a), b), 1., 2., etc.)
- Auto-determines question types:
  - `text` - Open-ended questions
  - `integer` - Numeric questions (age, count, years)
  - `date` - Date questions (birth date, etc.)
  - `select_one` - Single choice questions
  - `select_multiple` - Multiple choice questions

**Algorithm:**
1. Iterates through document paragraphs
2. Identifies questions by number patterns
3. Collects choice options below questions
4. Determines type based on text keywords and choices
5. Returns structured JSON format

### Excel Converter (utils/json_to_excel_converter.py)
**Functionality:**
- Creates surveyCTO-compatible Excel format
- Two sheets: "survey" and "choices"
- Proper column headers and styling
- Auto-adjusts column widths

**Survey Sheet Columns:**
- type - Question type
- name - Variable name
- label - Question text
- required - yes/no
- constraint - Validation rules
- relevant - Display logic
- appearance - UI appearance
- hint - Help text

**Choices Sheet Columns:**
- list_name - Choice list identifier
- name - Choice value
- label - Choice display text

## Data Flow

1. **User uploads .docx questionnaire**
   ↓
2. **DOCX Parser** extracts questions and choices
   ↓
3. **JSON structure** created with question metadata
   ↓
4. **User downloads JSON** file
   ↓
5. **User uploads JSON** file
   ↓
6. **Excel Converter** creates surveyCTO format
   ↓
7. **User downloads Excel** file ready for surveyCTO

## Question Type Detection

The parser uses keyword matching and structural analysis:

| Type | Detection Logic |
|------|----------------|
| `text` | Default for questions without choices |
| `integer` | Contains "number", "how many", "years" |
| `date` | Contains "date", "birth" |
| `select_one` | Has choices, not select_multiple |
| `select_multiple` | Contains "select all", "check all" |

## Configuration

### Dependencies (requirements.txt)
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - File upload support
- `python-docx` - DOCX parsing
- `openpyxl` - Excel file generation
- `pydantic` - Data validation

### Environment
- Default port: 8000
- Upload directory: `uploads/` (gitignored)
- Output directory: `output/` (gitignored)

## Error Handling

- Invalid file types → 400 Bad Request
- File not found → 404 Not Found
- Processing errors → 500 Internal Server Error
- Proper cleanup on errors (temp files removed)

## Security Features

- File type validation
- Specific exception handling
- CORS configuration (needs production adjustment)
- No execution of uploaded content
- Temporary file cleanup

## Testing

All endpoints tested with:
- Valid DOCX files with various question types
- Invalid file types (validation)
- Complete workflow (DOCX → JSON → Excel)
- File downloads
- Error conditions

All tests pass successfully! ✅

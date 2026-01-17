from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import json
from datetime import datetime
from utils.json_to_excel_converter import convert_json_to_excel

router = APIRouter()

# Ensure upload and output directories exist
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post("/convert/json-to-excel")
async def convert_json_to_excel_endpoint(file: UploadFile = File(...)):
    """
    Convert a JSON questionnaire file to surveyCTO ready Excel format.
    
    Upload a JSON file (previously generated from docx conversion) and receive
    an Excel file formatted for surveyCTO.
    """
    # Validate file type
    if not file.filename or not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Only .json files are supported")
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    upload_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")
    
    try:
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read JSON data
        with open(upload_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        
        # Convert to Excel
        excel_filename = f"{timestamp}_surveyCTO.xlsx"
        excel_path = os.path.join(OUTPUT_DIR, excel_filename)
        
        convert_json_to_excel(json_data, excel_path)
        
        # Clean up uploaded json
        os.remove(upload_path)
        
        return {
            "status": "success",
            "message": "JSON file converted to Excel successfully",
            "download_filename": excel_filename,
            "download_url": f"/api/download/excel/{excel_filename}"
        }
    
    except json.JSONDecodeError:
        # Clean up on error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        raise HTTPException(status_code=400, detail="Invalid JSON file format")
    
    except Exception as e:
        # Clean up on error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/download/excel/{filename}")
async def download_excel(filename: str):
    """
    Download a generated Excel file.
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

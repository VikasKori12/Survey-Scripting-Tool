from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os
import shutil
import json
from datetime import datetime
from utils.docx_parser import parse_docx_to_json

router = APIRouter()

# Ensure upload and output directories exist
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@router.post("/convert/docx-to-json")
async def convert_docx_to_json(file: UploadFile = File(...)):
    """
    Convert a .docx questionnaire file to JSON format.
    
    Upload a .docx file and receive a JSON representation of the questionnaire.
    The JSON can then be downloaded and used for the next conversion step.
    """
    # Validate file type
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    upload_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")
    
    try:
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse docx to json
        json_data = parse_docx_to_json(upload_path)
        
        # Save JSON file
        json_filename = f"{timestamp}_questionnaire.json"
        json_path = os.path.join(OUTPUT_DIR, json_filename)
        
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=2, ensure_ascii=False)
        
        # Clean up uploaded docx
        os.remove(upload_path)
        
        return {
            "status": "success",
            "message": "DOCX file converted to JSON successfully",
            "json_data": json_data,
            "download_filename": json_filename,
            "download_url": f"/api/download/json/{json_filename}"
        }
    
    except Exception as e:
        # Clean up on error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/download/json/{filename}")
async def download_json(filename: str):
    """
    Download a generated JSON file.
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/json"
    )

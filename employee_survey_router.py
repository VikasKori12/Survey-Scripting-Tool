"""
Router for employee survey parsing endpoint.
Converts .docx employee survey documents to JSON format.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from employee_survey_parser import extract_survey_units

router = APIRouter()

@router.post("/parse-employee-survey")
async def parse_employee_survey(file: UploadFile = File(...)):
    """
    Parse employee survey .docx file and convert to JSON.
    
    Expected format:
    - Scale definitions (5-point scales) at the top of sections
    - Multiple statements/questions using those scales
    - Demographic questions at the end
    
    Returns JSON array of survey units.
    """
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported.")
    
    content = await file.read()
    
    try:
        result = extract_survey_units(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse document: {str(e)}")
    
    return JSONResponse(result)

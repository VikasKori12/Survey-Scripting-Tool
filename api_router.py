
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from survey_parser import extract_survey_units

router = APIRouter()

@router.post("/parse-questionnaire")
async def parse_questionnaire(file: UploadFile = File(...)):
	if not file.filename.lower().endswith(".docx"):
		raise HTTPException(status_code=400, detail="Only .docx files are supported.")
	content = await file.read()
	try:
		result = extract_survey_units(content)
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"Failed to parse document: {e}")
	return JSONResponse(result)

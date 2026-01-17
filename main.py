

from fastapi import FastAPI
from api_router import router as api_router
from json_to_excel_router import router as excel_router
from employee_survey_router import router as employee_survey_router
from employee_json_to_excel_router import router as employee_excel_router

app = FastAPI()
app.include_router(api_router)
app.include_router(excel_router)
app.include_router(employee_survey_router)
app.include_router(employee_excel_router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import docx_router, excel_router

app = FastAPI(
    title="Survey Scripting Tool",
    description="Convert .docx questionnaire to JSON and then to surveyCTO ready Excel",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(docx_router.router, prefix="/api", tags=["DOCX to JSON"])
app.include_router(excel_router.router, prefix="/api", tags=["JSON to Excel"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Survey Scripting Tool API",
        "endpoints": {
            "docx_to_json": "/api/convert/docx-to-json",
            "json_to_excel": "/api/convert/json-to-excel",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

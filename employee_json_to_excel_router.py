"""
Router for converting employee survey JSON to SurveyCTO Excel format.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import json
import io
import openpyxl

router = APIRouter()

@router.post("/employee-json-to-surveycto-excel")
async def employee_json_to_surveycto_excel(file: UploadFile = File(...)):
    """
    Convert employee survey JSON to SurveyCTO Excel format.
    
    Expects JSON array of survey units with:
    - type: question type (select_one, select_multiple, text, integer, note)
    - field_name: unique field identifier
    - question_text: the question/statement text
    - choices: list of choices (for select_one/select_multiple)
    - choice_list_name: name of the choice list (for scales)
    - appearance: (kept blank)
    - relevance: (kept blank)
    - required: yes/no/empty
    """
    if not file.filename.lower().endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files are supported.")
    
    content = await file.read()
    
    try:
        data = json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    
    # Expecting a list of dicts
    if not isinstance(data, list):
        raise HTTPException(status_code=400, detail="JSON must be a list of survey units.")
    
    if data and not isinstance(data[0], dict):
        raise HTTPException(status_code=400, detail="JSON must be a list of survey units (dicts).")
    
    # Prepare workbook
    wb = openpyxl.Workbook()
    ws_survey = wb.active
    ws_survey.title = "survey"
    ws_choices = wb.create_sheet("choices")
    
    # Survey sheet columns
    survey_columns = ["type", "name", "label", "appearance", "relevance", "required"]
    ws_survey.append(survey_columns)
    
    # Choices sheet columns
    ws_choices.append(["list_name", "value", "label"])
    
    # Map: tuple(choices) -> choice_list_name
    choices_map = {}
    choices_dict = {}
    choice_list_name_counter = 1
    
    for unit in data:
        qtype = unit.get("type", "")
        field_name = unit.get("field_name", "")
        label = unit.get("question_text", "")
        appearance = unit.get("appearance", "") or ""
        relevance = unit.get("relevance", "") or ""
        required = unit.get("required", "") or ""
        choices = unit.get("choices", [])
        choice_list_name = unit.get("choice_list_name", "")
        
        # For select_one/select_multiple, assign consistent choice_list_name
        if qtype in ("select_one", "select_multiple") and choices:
            choices_tuple = tuple([str(c).strip() for c in choices])
            
            # Use provided choice_list_name if available, otherwise generate
            if choice_list_name and choice_list_name not in choices_dict.values():
                # Use the provided name
                choices_map[choices_tuple] = choice_list_name
                choices_dict[choice_list_name] = list(choices_tuple)
                final_choice_list_name = choice_list_name
            elif choices_tuple in choices_map:
                # Reuse existing choice list
                final_choice_list_name = choices_map[choices_tuple]
            else:
                # Create new choice list name
                base_name = choice_list_name or (field_name + "_list")
                name = base_name
                while name in choices_dict.values():
                    name = f"{base_name}_{choice_list_name_counter}"
                    choice_list_name_counter += 1
                choices_map[choices_tuple] = name
                choices_dict[name] = list(choices_tuple)
                final_choice_list_name = name
            
            survey_type = f"{qtype} {final_choice_list_name}"
        else:
            survey_type = qtype
        
        ws_survey.append([
            survey_type,
            field_name,
            label,
            appearance,
            relevance,
            required
        ])
    
    # Write choices sheet
    for list_name, choice_list in choices_dict.items():
        for idx, label in enumerate(choice_list, 1):
            ws_choices.append([list_name, idx, label])
    
    # Save to bytes
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=employee_surveyCTO.xlsx"}
    )

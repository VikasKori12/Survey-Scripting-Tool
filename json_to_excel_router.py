from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import json
import io
import openpyxl

router = APIRouter()

@router.post("/json-to-surveycto-excel")
async def json_to_surveycto_excel(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".json"):
        raise HTTPException(status_code=400, detail="Only .json files are supported.")
    content = await file.read()
    try:
        data = json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
    # Expecting a list of dicts or list of lists
    if isinstance(data, list) and data and isinstance(data[0], list):
        # List of lists: flatten
        data = [item for sublist in data for item in sublist]
    elif isinstance(data, list):
        pass
    else:
        raise HTTPException(status_code=400, detail="JSON must be a list of survey units.")

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
        appearance = unit.get("appearance", "")
        relevance = unit.get("relevance", "")
        required = unit.get("required", "")
        choices = unit.get("choices", [])
        # For select_one/select_multiple, assign consistent choice_list_name
        if qtype in ("select_one", "select_multiple") and choices:
            choices_tuple = tuple([str(c).strip() for c in choices])
            if choices_tuple not in choices_map:
                # Assign a new name
                base_name = unit.get("choice_list_name") or (field_name + "_list")
                # Ensure uniqueness
                name = base_name
                while name in choices_dict.values():
                    name = f"{base_name}_{choice_list_name_counter}"
                    choice_list_name_counter += 1
                choices_map[choices_tuple] = name
                choices_dict[name] = list(choices_tuple)
            choice_list_name = choices_map[choices_tuple]
            survey_type = f"{qtype} {choice_list_name}"
        else:
            choice_list_name = ""
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
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename=surveyCTO.xlsx"})

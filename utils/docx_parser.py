from docx import Document
from typing import List, Dict, Any
import re


def parse_docx_to_json(file_path: str) -> Dict[str, Any]:
    """
    Parse a .docx questionnaire file and convert it to JSON format.
    
    Expected format:
    - Questions can be numbered (e.g., "1. What is your name?")
    - Question types can be inferred from context or specified
    - Multiple choice options should be on separate lines starting with letters/numbers
    
    Returns a structured JSON with survey questions.
    """
    doc = Document(file_path)
    questions = []
    current_question = None
    current_choices = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        if not text:
            # Empty line might indicate end of a question
            if current_question:
                # Finalize the question type
                if current_choices:
                    current_question['choices'] = current_choices
                    # Update type based on question text and presence of choices
                    question_type = determine_question_type(current_question['question'])
                    if question_type == 'select_multiple':
                        current_question['type'] = 'select_multiple'
                    else:
                        # Has choices but not explicitly select_multiple, so select_one
                        current_question['type'] = 'select_one'
                else:
                    # No choices, so use question text to determine type
                    current_question['type'] = determine_question_type(current_question['question'])
                questions.append(current_question)
                current_question = None
                current_choices = []
            continue
        
        # Check if this is a question (starts with number or "Q")
        question_match = re.match(r'^(\d+\.?|Q\d+\.?)\s+(.+)', text, re.IGNORECASE)
        if question_match:
            # Save previous question if exists
            if current_question:
                # Finalize the question type
                if current_choices:
                    current_question['choices'] = current_choices
                    # Update type based on question text and presence of choices
                    question_type = determine_question_type(current_question['question'])
                    if question_type == 'select_multiple':
                        current_question['type'] = 'select_multiple'
                    else:
                        # Has choices but not explicitly select_multiple, so select_one
                        current_question['type'] = 'select_one'
                else:
                    # No choices, so use question text to determine type
                    current_question['type'] = determine_question_type(current_question['question'])
                questions.append(current_question)
            
            question_num = question_match.group(1).rstrip('.')
            question_text = question_match.group(2)
            
            current_question = {
                'id': f'q{question_num}',
                'question': question_text,
                'type': 'text',  # Will be updated if choices are found
                'required': True
            }
            current_choices = []
        
        # Check if this is a choice option (a), b), 1), etc.)
        elif current_question:
            choice_match = re.match(r'^([a-z]\)|[a-z]\.|[\d]+\)|\d+\.)\s*(.+)', text, re.IGNORECASE)
            if choice_match:
                choice_text = choice_match.group(2)
                current_choices.append(choice_text)
            elif not question_match:
                # Continuation of question or additional info
                if 'description' not in current_question:
                    current_question['description'] = text
                else:
                    current_question['description'] += ' ' + text
    
    # Don't forget the last question
    if current_question:
        # Finalize the question type
        if current_choices:
            current_question['choices'] = current_choices
            # Update type based on question text and presence of choices
            question_type = determine_question_type(current_question['question'])
            if question_type == 'select_multiple':
                current_question['type'] = 'select_multiple'
            else:
                # Has choices but not explicitly select_multiple, so select_one
                current_question['type'] = 'select_one'
        else:
            # No choices, so use question text to determine type
            current_question['type'] = determine_question_type(current_question['question'])
        questions.append(current_question)
    
    return {
        'survey_name': 'Questionnaire',
        'version': '1.0',
        'questions': questions
    }


def determine_question_type(question_text: str) -> str:
    """
    Determine the type of question based on the question text.
    """
    lower_text = question_text.lower()
    
    if 'select all' in lower_text or 'check all' in lower_text or 'select all that apply' in lower_text:
        return 'select_multiple'
    elif 'date' in lower_text or 'birth' in lower_text:
        return 'date'
    elif 'number' in lower_text or 'how many' in lower_text or 'years' in lower_text:
        return 'integer'
    else:
        # Default to text for open-ended questions
        return 'text'

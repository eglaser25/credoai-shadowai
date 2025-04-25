import json
from typing import Dict, Any, List
from datetime import datetime
import uuid

def validate_use_case(use_case: Dict[str, Any]) -> List[str]:
    """Validate a use case against the Credo AI schema"""
    errors = []
    
    # Required fields
    required_fields = [
        "id", "name", "description", "ai_type", "governance_status",
        "domains", "industries", "regions", "custom_fields", "questionnaires",
        "inserted_at", "updated_at"
    ]
    
    for field in required_fields:
        if field not in use_case:
            errors.append(f"Missing required field: {field}")
    
    # Validate field types
    if "id" in use_case and not isinstance(use_case["id"], str):
        errors.append("id must be a string")
    
    if "name" in use_case and not isinstance(use_case["name"], str):
        errors.append("name must be a string")
    
    if "description" in use_case and not isinstance(use_case["description"], (str, type(None))):
        errors.append("description must be a string or null")
    
    if "ai_type" in use_case and not isinstance(use_case["ai_type"], str):
        errors.append("ai_type must be a string")
    
    if "governance_status" in use_case and not isinstance(use_case["governance_status"], str):
        errors.append("governance_status must be a string")
    elif "governance_status" in use_case and use_case["governance_status"] not in ["unknown", "under_review", "approved", "rejected"]:
        errors.append("governance_status must be one of: unknown, under_review, approved, rejected")
    
    if "domains" in use_case and not isinstance(use_case["domains"], list):
        errors.append("domains must be an array")
    elif "domains" in use_case:
        for item in use_case["domains"]:
            if not isinstance(item, str):
                errors.append("domains items must be strings")
    
    if "industries" in use_case and not isinstance(use_case["industries"], list):
        errors.append("industries must be an array")
    elif "industries" in use_case:
        for item in use_case["industries"]:
            if not isinstance(item, str):
                errors.append("industries items must be strings")
    
    if "regions" in use_case and not isinstance(use_case["regions"], list):
        errors.append("regions must be an array")
    elif "regions" in use_case:
        for item in use_case["regions"]:
            if not isinstance(item, str):
                errors.append("regions items must be strings")
    
    if "custom_fields" in use_case:
        if not isinstance(use_case["custom_fields"], list):
            errors.append("custom_fields must be an array")
        else:
            for cf in use_case["custom_fields"]:
                if not all(k in cf for k in ["custom_field_id", "type", "name", "value"]):
                    errors.append("custom_field must have custom_field_id, type, name, and value")
                if not isinstance(cf["custom_field_id"], str):
                    errors.append("custom_field_id must be a string")
                if not isinstance(cf["type"], str):
                    errors.append("custom_field type must be a string")
                if not isinstance(cf["name"], str):
                    errors.append("custom_field name must be a string")
                if not isinstance(cf["value"], (bool, int, float, str, type(None))):
                    errors.append("custom_field value must be boolean, number, string, or null")
    
    if "questionnaires" in use_case:
        if not isinstance(use_case["questionnaires"], list):
            errors.append("questionnaires must be an array")
        else:
            for q in use_case["questionnaires"]:
                if not all(k in q for k in ["name", "key", "version", "sections"]):
                    errors.append("questionnaire must have name, key, version, and sections")
                if not isinstance(q["name"], str):
                    errors.append("questionnaire name must be a string")
                if not isinstance(q["key"], str):
                    errors.append("questionnaire key must be a string")
                if not isinstance(q["version"], (int, float)):
                    errors.append("questionnaire version must be a number")
                if not isinstance(q["sections"], list):
                    errors.append("questionnaire sections must be an array")
                else:
                    for s in q["sections"]:
                        if not all(k in s for k in ["id", "title", "questions"]):
                            errors.append("section must have id, title, and questions")
                        if not isinstance(s["id"], str):
                            errors.append("section id must be a string")
                        if not isinstance(s["title"], str):
                            errors.append("section title must be a string")
                        if not isinstance(s["questions"], list):
                            errors.append("section questions must be an array")
                        else:
                            for q in s["questions"]:
                                if not all(k in q for k in ["id", "answer"]):
                                    errors.append("question must have id and answer")
                                if not isinstance(q["id"], str):
                                    errors.append("question id must be a string")
                                if not isinstance(q["answer"], (bool, int, float, str, dict, type(None))):
                                    errors.append("question answer must be boolean, number, string, object, or null")
    
    if "inserted_at" in use_case and not isinstance(use_case["inserted_at"], str):
        errors.append("inserted_at must be a string")
    
    if "updated_at" in use_case and not isinstance(use_case["updated_at"], str):
        errors.append("updated_at must be a string")
    
    return errors

def format_use_case(use_case: Dict[str, Any]) -> Dict[str, Any]:
    """Format a use case to match the Credo AI schema"""
    # Ensure all required fields are present
    formatted = {
        "id": use_case.get("id", str(uuid.uuid4())),
        "name": use_case.get("name", ""),
        "description": use_case.get("description", ""),
        "ai_type": use_case.get("ai_type", ""),
        "governance_status": "under_review",  # Default to under_review
        "domains": use_case.get("domains", []),
        "industries": use_case.get("industries", []),
        "regions": use_case.get("regions", []),
        "custom_fields": use_case.get("custom_fields", []),
        "questionnaires": use_case.get("questionnaires", []),
        "inserted_at": use_case.get("inserted_at", datetime.now().isoformat() + "Z"),
        "updated_at": use_case.get("updated_at", datetime.now().isoformat() + "Z")
    }
    
    # Add optional fields if they exist
    if "risk_category_level" in use_case:
        formatted["risk_classification_level"] = use_case["risk_category_level"]
    if "icon" in use_case:
        formatted["icon"] = use_case["icon"]
    
    # Ensure custom_fields have all required fields
    formatted["custom_fields"] = [
        {
            "custom_field_id": cf.get("custom_field_id", str(uuid.uuid4())),
            "type": cf.get("type", "string"),
            "name": cf.get("name", ""),
            "value": cf.get("value", None)
        }
        for cf in formatted["custom_fields"]
    ]
    
    # Ensure questionnaires have all required fields
    formatted["questionnaires"] = [
        {
            "name": q.get("name", "Default Questionnaire"),
            "key": q.get("key", "default_questionnaire"),
            "version": q.get("version", 1.0),
            "sections": [
                {
                    "id": s.get("id", str(uuid.uuid4())),
                    "title": s.get("title", "Default Section"),
                    "questions": [
                        {
                            "id": q.get("id", str(uuid.uuid4())),
                            "answer": q.get("answer", None)
                        }
                        for q in s.get("questions", [])
                    ]
                }
                for s in q.get("sections", [])
            ]
        }
        for q in formatted["questionnaires"]
    ]
    
    return formatted

def format_use_cases(use_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Format multiple use cases to match the Credo AI schema"""
    formatted_cases = []
    for use_case in use_cases:
        formatted = format_use_case(use_case)
        errors = validate_use_case(formatted)
        if errors:
            print(f"Warning: Use case {formatted['id']} has validation errors: {errors}")
        formatted_cases.append(formatted)
    return formatted_cases 
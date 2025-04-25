import json
import logging
from typing import Dict, Any, List
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrictValidator:
    def __init__(self):
        self.errors = []
        
    def validate_use_case(self, use_case: Dict[str, Any]) -> bool:
        """Validate a single use case against the schema"""
        self.errors = []
        
        # Required fields
        required_fields = {
            "id": str,
            "name": str,
            "description": (str, type(None)),
            "ai_type": str,
            "governance_status": int,
            "domains": list,
            "industries": list,
            "regions": list,
            "custom_fields": list,
            "questionnaires": list,
            "inserted_at": str,
            "updated_at": str
        }
        
        # Check required fields
        for field, expected_type in required_fields.items():
            if field not in use_case:
                self.errors.append(f"Missing required field: {field}")
                continue
                
            if not isinstance(use_case[field], expected_type):
                self.errors.append(f"Field {field} has wrong type. Expected {expected_type}, got {type(use_case[field])}")
        
        # Check arrays contain correct types
        for field in ["domains", "industries", "regions"]:
            if field in use_case:
                for item in use_case[field]:
                    if not isinstance(item, str):
                        self.errors.append(f"Item in {field} array is not a string: {item}")
        
        # Validate custom fields
        if "custom_fields" in use_case:
            for cf in use_case["custom_fields"]:
                self._validate_custom_field(cf)
        
        # Validate questionnaires
        if "questionnaires" in use_case:
            for q in use_case["questionnaires"]:
                self._validate_questionnaire(q)
        
        # Check for extra fields
        allowed_fields = set(required_fields.keys()) | {
            "use_case_number", "icon", "monetary_value", "in_review", 
            "risk_classification_level", "custom_fields", "questionnaires"
        }
        extra_fields = set(use_case.keys()) - allowed_fields
        if extra_fields:
            self.errors.append(f"Extra fields not allowed: {extra_fields}")
        
        return len(self.errors) == 0
    
    def _validate_custom_field(self, cf: Dict[str, Any]) -> None:
        """Validate a custom field"""
        required_fields = {
            "custom_field_id": str,
            "type": str,
            "name": str,
            "value": (bool, int, float, str, type(None))
        }
        
        for field, expected_type in required_fields.items():
            if field not in cf:
                self.errors.append(f"Custom field missing required field: {field}")
                continue
                
            if not isinstance(cf[field], expected_type):
                self.errors.append(f"Custom field {field} has wrong type. Expected {expected_type}, got {type(cf[field])}")
        
        # Check for extra fields
        allowed_fields = set(required_fields.keys())
        extra_fields = set(cf.keys()) - allowed_fields
        if extra_fields:
            self.errors.append(f"Custom field has extra fields not allowed: {extra_fields}")
    
    def _validate_questionnaire(self, q: Dict[str, Any]) -> None:
        """Validate a questionnaire"""
        required_fields = {
            "name": str,
            "key": str,
            "version": (int, float),
            "sections": list
        }
        
        for field, expected_type in required_fields.items():
            if field not in q:
                self.errors.append(f"Questionnaire missing required field: {field}")
                continue
                
            if not isinstance(q[field], expected_type):
                self.errors.append(f"Questionnaire {field} has wrong type. Expected {expected_type}, got {type(q[field])}")
        
        # Validate sections
        if "sections" in q:
            for section in q["sections"]:
                self._validate_section(section)
        
        # Check for extra fields
        allowed_fields = set(required_fields.keys())
        extra_fields = set(q.keys()) - allowed_fields
        if extra_fields:
            self.errors.append(f"Questionnaire has extra fields not allowed: {extra_fields}")
    
    def _validate_section(self, section: Dict[str, Any]) -> None:
        """Validate a section"""
        required_fields = {
            "id": str,
            "title": str,
            "questions": list
        }
        
        for field, expected_type in required_fields.items():
            if field not in section:
                self.errors.append(f"Section missing required field: {field}")
                continue
                
            if not isinstance(section[field], expected_type):
                self.errors.append(f"Section {field} has wrong type. Expected {expected_type}, got {type(section[field])}")
        
        # Validate questions
        if "questions" in section:
            for question in section["questions"]:
                self._validate_question(question)
        
        # Check for extra fields
        allowed_fields = set(required_fields.keys())
        extra_fields = set(section.keys()) - allowed_fields
        if extra_fields:
            self.errors.append(f"Section has extra fields not allowed: {extra_fields}")
    
    def _validate_question(self, question: Dict[str, Any]) -> None:
        """Validate a question"""
        required_fields = {
            "id": str,
            "answer": (bool, int, float, str, dict, type(None))
        }
        
        for field, expected_type in required_fields.items():
            if field not in question:
                self.errors.append(f"Question missing required field: {field}")
                continue
                
            if not isinstance(question[field], expected_type):
                self.errors.append(f"Question {field} has wrong type. Expected {expected_type}, got {type(question[field])}")
        
        # Check for extra fields
        allowed_fields = set(required_fields.keys())
        extra_fields = set(question.keys()) - allowed_fields
        if extra_fields:
            self.errors.append(f"Question has extra fields not allowed: {extra_fields}")

def validate_file(input_file: str) -> None:
    """Validate a JSON file against the schema"""
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        validator = StrictValidator()
        
        # Handle both single use case and array of use cases
        use_cases = data if isinstance(data, list) else [data]
        
        for i, use_case in enumerate(use_cases):
            logger.info(f"\nValidating use case {i+1}:")
            if validator.validate_use_case(use_case):
                logger.info("✓ Valid")
            else:
                logger.error("✗ Invalid:")
                for error in validator.errors:
                    logger.error(f"  - {error}")
    
    except Exception as e:
        logger.error(f"Error validating file: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        validate_file(sys.argv[1])
    else:
        print("Usage: python strict_validator.py <input_file>") 
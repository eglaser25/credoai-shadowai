import json
import logging
from typing import List, Dict, Any
import os
from datetime import datetime, UTC
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UseCaseFormatter:
    def __init__(self):
        self.output_file = "formatted_use_cases.json"
        self.api_url = "https://api.credo.ai/api/v2/credoai/use_cases"
        self.api_key = os.getenv("CREDO_AI_API_KEY")
        if not self.api_key:
            logger.error("CREDO_AI_API_KEY environment variable not set")
            raise ValueError("CREDO_AI_API_KEY environment variable not set")

    def read_logs(self, log_file: str) -> List[Dict[str, Any]]:
        """Read AI use case logs from JSON file"""
        try:
            logger.info(f"Reading from input file: {log_file}")
            with open(log_file, 'r') as f:
                data = json.load(f)
            logger.info(f"Read {len(data)} use cases from input file")
            return data
        except Exception as e:
            logger.error(f"Error reading log file: {e}")
            return []

    def format_use_case(self, use_case):
        """Format a use case according to the schema."""
        formatted = {
            "name": use_case["name"],
            "description": use_case["description"],
            "ai_type": "gen_ai",
            "governance_status": 1,
            "domains": [],
            "industries": [],
            "regions": [],
            "risk_classification_level": 1,
            "questionnaires": []
        }
        return formatted

    def format_use_cases(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format all log entries to match Credo AI schema exactly"""
        formatted_cases = [self.format_use_case(log) for log in logs]
        # Try a different payload structure
        return {
            "use_cases": formatted_cases
        }

    def save_formatted_cases(self, formatted_data: Dict[str, Any]) -> bool:
        """Save formatted use cases to a JSON file"""
        try:
            logger.info(f"Saving to output file: {self.output_file}")
            # Print the formatted JSON for debugging
            logger.info("Generated JSON:")
            logger.info(json.dumps(formatted_data, indent=2))
            
            with open(self.output_file, 'w') as f:
                json.dump(formatted_data, f, indent=2)
            logger.info(f"Successfully saved {len(formatted_data['use_cases'])} formatted use cases to {self.output_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving formatted use cases: {e}")
            return False

    def validate_use_cases(self, formatted_data: Dict[str, Any]) -> bool:
        """Validate the formatted use cases before sending to API"""
        try:
            items = formatted_data.get("use_cases", [])
            if not items:
                logger.error("No use cases found in formatted data")
                return False
            
            for i, item in enumerate(items):
                name = item.get("name", "").strip()
                if not name:
                    logger.error(f"Use case {i} has an empty name")
                    return False
                
                # Log the name for debugging
                logger.info(f"Validating use case {i} name: {repr(name)}")
            
            return True
        except Exception as e:
            logger.error(f"Error validating use cases: {str(e)}")
            return False

    def _set_custom_fields(self, use_case_id: str) -> bool:
        """Set custom fields for a use case after creation"""
        try:
            url = f"{self.api_url}/{use_case_id}/custom_fields"
            headers = {
                "Authorization": self.api_key,
                "Content-Type": "application/json"
            }
            
            # Prepare the payload
            payload = {
                "custom_fields": {
                    "dDWtfWDZAL6fFmMKpppHLE": "ShadowAI"
                }
            }
            
            logging.info(f"Setting custom fields for use case {use_case_id}")
            logging.info(f"Custom fields payload: {json.dumps(payload, indent=2)}")
            
            response = requests.put(url, headers=headers, json=payload)
            
            logging.info(f"Custom fields response status: {response.status_code}")
            logging.info(f"Custom fields response: {response.text}")
            
            return response.status_code in [200, 201]
        except Exception as e:
            logging.error(f"Error setting custom fields: {str(e)}")
            return False

    def upload_use_cases(self):
        """Upload use cases to Credo AI."""
        if not self.formatted_use_cases:
            logging.error("No formatted use cases to upload")
            return

        logging.info(f"Using API URL: {self.api_url}")
        logging.info(f"Using API key: {self.api_key[:3]}...")

        for i, use_case in enumerate(self.formatted_use_cases["use_cases"], 1):
            logging.info(f"Uploading use case {i} of {len(self.formatted_use_cases['use_cases'])}")
            
            payload = use_case.copy()
            
            try:
                name = use_case["name"]
                logging.info(f"Raw data before encoding:")
                logging.info(json.dumps(payload, indent=2))
                
                encoded_data = json.dumps(payload).encode('utf-8')
                logging.info(f"Encoded data (first 100 chars):")
                logging.info(encoded_data[:100])
                
                logging.info(f"Uploading use case with name: {name}")
                
                headers = {
                    'Authorization': self.api_key,
                    'Content-Type': 'application/json'
                }
                
                response = requests.post(self.api_url, data=encoded_data, headers=headers)
                
                logging.info(f"Response status code: {response.status_code}")
                logging.info(f"Response headers: {response.headers}")
                logging.info(f"Response body: {response.text}")
                
                if response.status_code == 422 and "name has already been taken" in response.text:
                    logging.info("Name already taken, trying with timestamp...")
                    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
                    payload["name"] = f"{name}_{timestamp}"
                    
                    logging.info(f"Raw data before encoding:")
                    logging.info(json.dumps(payload, indent=2))
                    
                    encoded_data = json.dumps(payload).encode('utf-8')
                    logging.info(f"Encoded data (first 100 chars):")
                    logging.info(encoded_data[:100])
                    
                    logging.info(f"Uploading use case with name: {payload['name']}")
                    
                    response = requests.post(self.api_url, data=encoded_data, headers=headers)
                    
                    logging.info(f"Response status code: {response.status_code}")
                    logging.info(f"Response headers: {response.headers}")
                    logging.info(f"Response body: {response.text}")
                
                if response.status_code in [200, 201]:
                    logging.info(f"Successfully uploaded use case {i}")
                    response_data = response.json()
                    use_case_id = response_data.get("data", {}).get("id")
                    logging.info(f"Created use case ID: {use_case_id}")
                    
                    # Set custom fields after successful creation
                    if use_case_id:
                        if self._set_custom_fields(use_case_id):
                            logging.info(f"Successfully set custom fields for use case {use_case_id}")
                        else:
                            logging.error(f"Failed to set custom fields for use case {use_case_id}")
                else:
                    logging.error(f"Failed to upload use case {i}")
                    logging.error(f"Status code: {response.status_code}")
                    logging.error(f"Response: {response.text}")
                    
            except Exception as e:
                logging.error(f"Error uploading use case {i}: {str(e)}")
                continue
        
        logging.info("Successfully processed use cases")

def main():
    # Get input file from environment variable or use default
    log_file = os.getenv("LOG_FILE", "ai_logs.json")
    dry_run = os.getenv("DRY_RUN", "true").lower() == "true"

    # Initialize formatter
    formatter = UseCaseFormatter()

    # Read and process logs
    logs = formatter.read_logs(log_file)
    if not logs:
        logger.error("No logs found or error reading logs")
        return

    # Format use cases
    formatted_data = formatter.format_use_cases(logs)
    
    # Save formatted cases to file
    success = formatter.save_formatted_cases(formatted_data)
    if not success:
        logger.error("Failed to save formatted use cases")
        return

    # Upload to API if not in dry run mode
    if not dry_run:
        formatter.formatted_use_cases = formatted_data
        formatter.upload_use_cases()

    logger.info("Successfully processed use cases")

if __name__ == "__main__":
    main() 
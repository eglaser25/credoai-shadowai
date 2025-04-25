# -*- coding: utf-8 -*-
import json
from datetime import datetime

# Load the input file
input_file = "/Users/evan/Downloads/user-activity-logs-clean/2024-12-16T22-29-31-214Z-2024-12-16T22-27-24-147Z.json"
output_file = "reformatted_use_cases.json"

# Governance status mapping
governance_mapping = {
    "REROUTE": 1,
    "INLINE_BLOCK": 2,
    "REDACT": 3
}

# Read input JSON file with debugging
try:
    with open(input_file, "r", encoding="utf-8") as f:
        logs = json.load(f)
except Exception as e:
    print("Error loading JSON file:", str(e))
    exit()

# Convert log entries to the schema format
use_cases = []

for log in logs:
    try:
        use_case = {
            "id": log.get("traceId", ""),
            "name": log.get("intent", {}).get("request", [{}])[0].get("actionName", "Unknown Use Case"),
            "description": log.get("intent", {}).get("request", [{}])[0].get("departmentName", "No description"),
            "ai_type": log.get("serviceName", "Unknown AI"),
            "governance_status": governance_mapping.get(log.get("policyDecision", {}).get("label", ""), 0),
            "domains": [],
            "industries": [log.get("intent", {}).get("request", [{}])[0].get("departmentName", "General")],
            "regions": [],
            "risk_category_level": None,
            "custom_fields": [
                {
                    "custom_field_id": "user_001",
                    "name": "User Name",
                    "value": log.get("userClaim", {}).get("name", "Unknown")
                },
                {
                    "custom_field_id": "email_001",
                    "name": "User Email",
                    "value": log.get("userClaim", {}).get("email", "Unknown")
                },
                {
                    "custom_field_id": "ip_001",
                    "name": "Client IP",
                    "value": log.get("clientIp", {}).get("remoteAddr", "Unknown")
                }
            ],
            "questionnaires": [],
            "inserted_at": datetime.utcfromtimestamp(log.get("startTime", 0) / 1000).isoformat() + "Z",
            "updated_at": datetime.utcfromtimestamp(log.get("endTime", 0) / 1000).isoformat() + "Z"
        }
        use_cases.append(use_case)
    except Exception as e:
        print("Error processing log:", log)
        print("Error message:", str(e))
        exit()

# Save reformatted JSON with debugging
try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(use_cases, f, indent=4)
    print("Reformatted JSON saved as", output_file)
except Exception as e:
    print("Error writing output JSON:", str(e))
    exit()

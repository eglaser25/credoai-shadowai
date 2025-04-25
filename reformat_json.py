import json
from datetime import datetime

# Load the input file
input_file = "2024-11-27T21-22-14-584Z-2024-11-27T19-08-09-738Z.json"
output_file = "reformatted_use_cases.json"

# Governance status mapping
governance_mapping = {
    "REROUTE": 1,
    "INLINE_BLOCK": 2,
    "REDACT": 3
}

# Read input JSON file
with open(input_file, "r") as f:
    logs = json.load(f)

# Convert log entries to the schema format
use_cases = []

for log in logs:
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

# Save reformatted JSON
with open(output_file, "w") as f:
    json.dump(use_cases, f, indent=4)

print(f"✅ Reformatted JSON saved as {output_file}")

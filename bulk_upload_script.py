import requests
import json

# API endpoint
url = "https://api.credo.ai/api/v2/credoai/use_cases/import"

# Replace with your actual API key
API_KEY = "87j1AJQxZim4UbB5todoicqV8C5kCVQVjP4eLGHJCQ9sPljBn5CFmEXIUMteuxHI"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Load JSON data
json_file = "reformatted_use_cases.json"
try:
    with open(json_file, "r") as f:
        data = json.load(f)
except Exception as e:
    print(f"❌ Error loading JSON file: {e}")
    exit()

# Debugging: Print the JSON data before sending
print("\n🔍 Sending the following JSON data:")
print(json.dumps(data, indent=4))

# Debugging: Check if data is an array
if not isinstance(data, list):
    print("\n⚠️ JSON data should be a list (array). Your data might be wrapped incorrectly.")
    exit()

# Send the request
response = requests.post(url, headers=headers, json=data)

# Debugging: Print response details
print("\n🔍 Response Details:")
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")
print(f"Response Headers: {response.headers}")

# Debugging: Show request details
print("\n🔍 Request Details:")
print(f"Request URL: {response.request.url}")
print(f"Request Headers: {response.request.headers}")
print(f"Request Body: {response.request.body}")

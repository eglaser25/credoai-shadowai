# Credo AI Shadow AI Detector

A Python tool for detecting and managing AI use cases, specifically designed to integrate with the Credo AI platform. This tool helps organizations track and manage their AI use cases by automatically formatting and uploading them to Credo AI.

## Features

- Reads AI use case logs from JSON files
- Formats use cases according to the Credo AI schema
- Validates use cases before upload
- Handles naming conflicts by appending timestamps
- Sets custom fields for tracking Shadow AI use cases
- Provides detailed logging for debugging
- Supports dry-run mode for testing

## Prerequisites

- Python 3.x
- Credo AI API key
- Basic understanding of JSON and API interactions

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/eglaser25/credoai-shadowai.git
   cd credoai-shadowai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Credo AI API key:
   ```
   CREDO_AI_API_KEY=your_api_key_here
   LOG_FILE=ai_logs.json
   DRY_RUN=true
   ```

## Usage

### Input File Format

The tool expects a JSON file containing an array of use cases. Each use case should have at least a `name` and `description`. Example:

```json
[
  {
    "name": "Customer Support Chatbot",
    "description": "AI-powered chatbot for handling customer inquiries"
  },
  {
    "name": "Document Analysis",
    "description": "AI system for analyzing and categorizing documents"
  }
]
```

### Running the Tool

1. Prepare your AI logs in JSON format (default: `ai_logs.json`)

2. Run the script:
   ```bash
   python shadow_ai_detector.py
   ```

3. Check the output:
   - Formatted use cases are saved to `formatted_use_cases.json`
   - Logs are printed to the console
   - If `DRY_RUN=true`, no actual upload occurs

### Configuration Options

The following environment variables can be set in your `.env` file:

- `CREDO_AI_API_KEY`: Your Credo AI API key (required)
- `LOG_FILE`: Path to your input JSON file (default: `ai_logs.json`)
- `DRY_RUN`: Set to `true` to test without uploading (default: `true`)

### Output

The tool generates:
1. `formatted_use_cases.json`: Contains the formatted use cases ready for upload
2. Console logs showing the progress and any errors
3. API responses for each upload attempt

## Error Handling

The tool includes comprehensive error handling for:
- Missing API keys
- Invalid JSON files
- API communication errors
- Name conflicts (automatically resolved with timestamps)
- Custom field setting failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
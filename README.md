# Shadow AI Detector

A Python tool for detecting and managing AI use cases, with integration to the Credo AI platform.

## Features

- Reads AI use case logs from JSON files
- Formats use cases according to Credo AI schema
- Uploads use cases to Credo AI platform
- Handles custom fields and naming conflicts
- Comprehensive logging and error handling

## Prerequisites

- Python 3.x
- Credo AI API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/shadow_ai.git
cd shadow_ai
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
export CREDO_AI_API_KEY="your_api_key_here"
export LOG_FILE="path_to_your_ai_logs.json"
export DRY_RUN="true"  # Set to "false" for actual uploads
```

## Usage

1. Prepare your AI logs in JSON format (see `ai_logs.json` for example)
2. Run the script:
```bash
python shadow_ai_detector.py
```

The script will:
- Read the input file
- Format the use cases
- Save formatted use cases to `formatted_use_cases.json`
- Upload to Credo AI (if DRY_RUN=false)

## Configuration

- `LOG_FILE`: Path to your AI logs JSON file
- `DRY_RUN`: Set to "true" to test without uploading
- `CREDO_AI_API_KEY`: Your Credo AI API key

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
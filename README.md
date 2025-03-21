# AI Code Generator

A web application that generates code files based on natural language prompts using AI. This tool helps developers quickly scaffold projects by describing what they want in plain English.

## Features

- Web interface for entering prompts
- AI-powered code generation using OpenAI
- Automatic file creation with appropriate folder structure
- Support for JavaScript, HTML, and CSS code generation
- Timestamped output to organize generated projects

## Installation

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd sample_code_generator_with_ai
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   OPENAI_BASE_URL=<your-openai-base-url>
   OPENAI_API_KEY=<your-openai-api-key>
   OPENAI_MODEL_ID=<model-id-to-use>  # e.g., gpt-3.5-turbo or gpt-4
   ```

## Usage

1. Start the application:

   ```bash
   python main.py
   ```

2. Open a web browser and navigate to `http://127.0.0.1:5000`

3. Enter a prompt describing the code you want to generate, for example:

   ```
   Create a simple to-do list application with HTML, CSS, and JavaScript
   ```

4. Click "Generate Code" and wait for the AI to process your request

5. The files will be automatically created in a timestamped directory

## How It Works

1. The user enters a prompt in the web interface
2. The application sends the prompt to the OpenAI API
3. A system prompt instructs the AI to generate code in a specific JSON format
4. The application parses the JSON response and creates the corresponding files
5. Files are organized in a timestamp-prefixed directory structure

## Project Structure

```
sample_code_generator_with_ai/
├── main.py              # Flask application entry point
├── prompts.py           # Contains system prompt for OpenAI
├── templates/           # HTML templates
│   └── index.html       # Web interface
├── static/              # Static assets
│   └── css/             # CSS stylesheets
│       └── styles.css   # Main stylesheet
├── requirements.txt     # Python dependencies
└── README.md            # This documentation
```

## Generated Projects

Generated code is stored in timestamped directories in the root folder:

```
sample_code_generator_with_ai/
├── 1650123456/         # Timestamp (UNIX time)
│   └── src/            # Generated project files
│       ├── index.html
│       ├── style.css
│       └── script.js
```

## Customization

You can modify the system prompt in `prompts.py` to:

- Change the technology stack
- Adjust the output format requirements
- Provide more specific instructions to the AI

## License

[MIT License](LICENSE)

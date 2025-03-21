from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
import json
import time
from prompts import SYSTEM_PROMPT

# load dotenv in the base root
load_dotenv()

# Point to the local server
openai.api_base = os.getenv("OPENAI_BASE_URL")        
openai.api_key = os.getenv("OPENAI_API_KEY")

def create_files_from_json(json_data):
  try:
    files = json_data.get('files', [])
    timestamp_prefix = str(int(time.time()))

    for file in files:
      path = os.path.join(timestamp_prefix, file.get('path').lstrip('/'))
      name = file.get('name')
      content = file.get('content')
      
      if not os.path.exists(path):
        os.makedirs(path)
      
      with open(os.path.join(path, name), 'w') as f:
        f.write(content)
        
    return {"message": "Files created successfully!"}
  except Exception as e:
    return {"message": f"Failed to create files: {str(e)}"}

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
  try:
    prompt = request.form['prompt']
    
    # Call OpenAI API with user's prompt
    completion = openai.ChatCompletion.create(
      model=os.getenv("OPENAI_MODEL_ID"),
      messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
      ],
      temperature=0.7,
    )
    
    # Extract the response content
    response_content = completion.choices[0].message.content
    
    try:
      # Remove the leading and trailing triple backticks and the "json" language identifier
      reformat_response_content = response_content.split('```json')[1].split('```')[0].strip('`\n')
      # Try to parse the response as JSON
      json_result = json.loads(reformat_response_content)
      
      # Create files from the JSON response
      created_response = create_files_from_json(json_result)

      return created_response
    
    except json.JSONDecodeError:
      # If the response isn't valid JSON, create a simpler response
      return jsonify({
        "message": "Code generated but in unexpected format",
        "files": [{
          "path": "/",
          "name": "response.txt",
          "content": response_content
        }]
      })
      
  except Exception as e:
    print(f"Error generating code: {str(e)}")
    return jsonify({'message': f'Code generation failed: {str(e)}'}), 500

if __name__ == '__main__':
  app.run(debug=True)
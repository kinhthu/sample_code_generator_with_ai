from flask import Flask, render_template, request, jsonify
import openai
from dotenv import load_dotenv
import os
import json
import time

# load dotenv in the base root
load_dotenv()

# Point to the local server
openai.api_base = os.getenv("OPENAI_BASE_URL")        
openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = """
You are a senior software engineer. Your responsibility is to generate code based on the following instruction.

<tech_stack>
  - Javascript, html, css
  - using node.js
</tech_stack>

<output_format>
  The format of response should be a JSON object with the following keys:
  ```json
  {{
    "message": "Code generated successfully!",
    "files": [
      {
        "path": "/src",
        "name": "index.js",
        "content": "console.log('Hello, world!');"
      }
    ]
  }}
  ```

  DO:
  - return the response only in ```json``` format

  DON'T:
  - include any other text outside of ```json```
</output_format>
"""

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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
      ],
      temperature=0.7,
    )
    
    # Extract the response content
    response_content = completion.choices[0].message.content
    
#     response_content = """```json\n{\n  \"message\": \"Code generated successfully!\",\n  \"files\": [\n    {\n      \"path\": \"/src\",\n      \"name\": \"index.html\",\n      \"content\": \"<!DOCTYPE html>\\n<html lang=\\\"en\\\">\\n<head>\\n  <meta charset=\\\"UTF-8\\\">\\n  <meta name=\\\"viewport\\\" content=\\\"width=device-width, initial-scale=1.0\\\">\\n  <title>Landing Page</title>\\n  <link rel=\\\"stylesheet\\\" href=\\\"styles.css\\\">\\n</head>\\n<body>\\n  <header>\\n    <h1>Welcome to Our Service!</h1>\\n  </header>\\n  <section class=\\\"banner\\\">\\n    <img src=\\\"banner.jpg\\\" alt=\\\"Banner Image\\\">\\n  </section>\\n  <section class=\\\"contact-form\\\">\\n    <form id=\\\"contactForm\\\">\\n      <label for=\\\"name\\\">Name:</label>\\n      <input type=\\\"text\\\" id=\\\"name\\\" name=\\\"name\\\" required>\\n      \\n      <label for=\\\"email\\\">Email:</label>\\n      <input type=\\\"email\\\" id=\\\"email\\\" name=\\\"email\\\" required>\\n      \\n      <label for=\\\"message\\\">Message:</label>\\n      <textarea id=\\\"message\\\" name=\\\"message\\\" rows=\\\"4\\\" required></textarea>\\n      \\n      <button type=\\\"submit\\\">Send</button>\\n    </form>\\n  </section>\\n  <script src=\\\"script.js\\\"></script>\\n</body>\\n</html>\"\n    },\n    {\n      \"path\": \"/src\",\n      \"name\": \"styles.css\",\n      \"content\": \"body {\\n  font-family: Arial, sans-serif;\\n  margin: 0;\\n  padding: 0;\\n}\\n\\nheader {\\n  background-color: #4CAF50;\\n  color: white;\\n  text-align: center;\\n  padding: 1em 0;\\n}\\n\\n.banner img {\\n  width: 100%;\\n  height: auto;\\n}\\n\\n.contact-form {\\n  max-width: 600px;\\n  margin: 2em auto;\\n  padding: 20px;\\n  background-color: #f4f4f9;\\n  border-radius: 8px;\\n}\\n\\nform label {\\n  display: block;\\n  margin-bottom: 5px;\\n}\\n\\nform input, form textarea {\\n  width: 100%;\\n  padding: 10px;\\n  margin-bottom: 20px;\\n  border: 1px solid #ccc;\\n  border-radius: 4px;\\n}\\n\\nbutton {\\n  background-color: #4CAF50;\\n  color: white;\\n  padding: 10px 15px;\\n  border: none;\\n  border-radius: 4px;\\n  cursor: pointer;\\n}\\n\\nbutton:hover {\\n  background-color: #45a049;\\n}\"\n    },\n    {\n      \"path\": \"/src\",\n      \"name\": \"script.js\",\n      \"content\": \"document.getElementById('contactForm').addEventListener('submit', function(event) {\\n  event.preventDefault();\\n  alert('Thank you for contacting us!');\\n});\"\n    }\n  ]\n}\n```
# """
  #   response_content = """Sure! Below is a JSON object representing the generated code for a simple landing page of a food restaurant. The files include `index.html`, `styles.css`, and `script.js` to handle basic functionality.\n\n```json\n{\n  \"message\": \"Code generated successfully!\",\n  \"files\": [\n    {\n      \"path\": \"/src\",\n      \"name\": \"index.html\",\n      \"content\": `\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>Delicious Meals</title>\n  <link rel=\"stylesheet\" href=\"styles.css\">\n</head>\n<body>\n  <header>\n    <h1>Welcome to Delicious Meals</h1>\n  </header>\n  <section class=\"banner\">\n    <img src=\"https://via.placeholder.com/1200x400?text=Delicious+Meals\" alt=\"Banner Image\">\n  </section>\n  <main>\n    <section class=\"meals\">\n      <h2>Our Delicious Meals</h2>\n      <div class=\"meal-grid\">\n        <img src=\"https://via.placeholder.com/300x300?text=Meal+1\" alt=\"Meal 1\">\n        <img src=\"https://via.placeholder.com/300x300?text=Meal+2\" alt=\"Meal 2\">\n        <img src=\"https://via.placeholder.com/300x300?text=Meal+3\" alt=\"Meal 3\">\n      </div>\n    </section>\n    <section class=\"contact\">\n      <h2>Contact Us</h2>\n      <form id=\"contactForm\">\n        <label for=\"name\">Name:</label>\n        <input type=\"text\" id=\"name\" name=\"name\" required>\n        \n        <label for=\"email\">Email:</label>\n        <input type=\"email\" id=\"email\" name=\"email\" required>\n        \n        <label for=\"message\">Message:</label>\n        <textarea id=\"message\" name=\"message\" rows=\"4\" required></textarea>\n        \n        <button type=\"submit\">Submit</button>\n      </form>\n    </section>\n  </main>\n  <footer>\n    <p>&copy; 2023 Delicious Meals. All rights reserved.</p>\n  </footer>\n  <script src=\"script.js\"></script>\n</body>\n</html>\n`\n    },\n    {\n      \"path\": \"/src\",\n      \"name\": \"styles.css\",\n      \"content\": `\nbody {\n  font-family: Arial, sans-serif;\n  margin: 0;\n  padding: 0;\n}\n\nheader {\n  background-color: #333;\n  color: white;\n  text-align: center;\n  padding: 1em 0;\n}\n\n.banner img {\n  width: 100%;\n  height: auto;\n}\n\n.meals {\n  text-align: center;\n  margin: 2em 0;\n}\n\n.meal-grid {\n  display: flex;\n  justify-content: space-around;\n  flex-wrap: wrap;\n}\n\n.meal-grid img {\n  max-width: 300px;\n  margin: 1em;\n}\n\n.contact {\n  max-width: 600px;\n  margin: 2em auto;\n  padding: 0 1em;\n}\n\nform {\n  display: flex;\n  flex-direction: column;\n}\n\nlabel {\n  margin-top: 1em;\n}\n\ninput, textarea {\n  padding: 0.5em;\n  font-size: 1em;\n}\n\nbutton {\n  margin-top: 1em;\n  padding: 0.5em;\n  background-color: #333;\n  color: white;\n  border: none;\n  cursor: pointer;\n}\n\nfooter {\n  text-align: center;\n  background-color: #333;\n  color: white;\n  padding: 1em 0;\n}\n`\n    },\n    {\n      \"path\": \"/src\",\n      \"name\": \"script.js\",\n      \"content\": `\ndocument.getElementById('contactForm').addEventListener('submit', function(event) {\n  event.preventDefault();\n  \n  const formData = new FormData(this);\n  const data = {};\n  \n  for (let [key, value] of formData.entries()) {\n    data[key] = value;\n  }\n  \n  console.log('Form Data:', data);\n  \n  alert('Thank you for your message!');\n});\n`\n    }\n  ]\n}\n```\n\nThis code creates a simple landing page with a banner image, a section displaying some delicious meal images, and a contact form. The CSS styles the page to be visually appealing, and the JavaScript handles the form submission by logging the data to the console and showing an alert to the user.
  # """
    try:
      # Remove the leading and trailing triple backticks and the "json" language identifier
      reformat_response_content = response_content.split('```json')[1].split('```')[0].strip('`\n')
      # Try to parse the response as JSON
      # print("format: " + reformat_response_content)
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
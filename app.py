from flask import Flask, render_template, request, jsonify, send_from_directory
import openai
import os

app = Flask(_name_)

# Set your OpenAI API key
openai.api_key=os.getenv('API_KEY')
# Serve the index.html from the same folder
@app.route("/")
def index():
    return send_from_directory(".", "index.html")  # Serve index.html from the current directory

# Serve JavaScript and CSS files
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)  # Serve static files (script.js, style.css)

# Endpoint to generate the image
@app.route("/generate-image", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get("description")
        if not prompt:
            return jsonify({"error": "Description is required"}), 400

        # Call OpenAI API to generate image
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response["data"][0]["url"]
        return jsonify({"image_url": image_url})

    except Exception as e:
        print("Error generating image:", e)
        return jsonify({"error": str(e)}), 500

if _name_ == "_main_":
    app.run(debug=True)
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = os.getenv('API_KEY')

@app.route("/generate-image", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get("description")
        
        if not prompt:
            return jsonify({"error": "Description is required"}), 400

        # Call OpenAI's API to generate an image
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512"
        )

        # Get the image URL
        image_url = response["data"][0]["url"]
        return jsonify({"image_url": image_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000)) 
    app.run(host='0.0.0.0', port=port, debug=True)

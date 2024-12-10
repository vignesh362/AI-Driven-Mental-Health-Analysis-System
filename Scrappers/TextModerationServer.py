from transformers import pipeline
from flask import Flask, request, jsonify
import requests
# Initialize Flask app
app = Flask(__name__)

# Load the moderation pipeline
print("Loading text moderation model...")
moderation_pipeline = pipeline("text-classification", model="KoalaAI/Text-Moderation")

@app.route("/moderate", methods=["POST"])
def moderate_text():
    """
    Endpoint to process text moderation.
    Accepts JSON with the format: {"text": "<your_text>"}
    """
    try:
        # Extract text from the request
        data = request.json
        if "text" not in data:
            return jsonify({"error": "Missing 'text' in request"}), 400

        text = data["text"]

        # Run the moderation model
        moderation_result = moderation_pipeline(text)

        # Return the result as JSON
        print("******************************************************")
        # print(moderation_result[0]["label"])
        return jsonify({
            "text": text,
            "moderation_result": moderation_result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server for text moderation...")
    app.run(host="0.0.0.0", port=8080)
from flask import Flask, request, jsonify
from transformers import pipeline

# Flask app initialization
app = Flask(__name__)

HF_TOKEN = "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"

# Load the model pipeline
print("Loading mental-roberta-base model...")
try:
    classification_pipeline = pipeline(
        "text-classification",
        model="mental/mental-roberta-base",
        use_auth_token=HF_TOKEN
    )
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

@app.route("/analyze", methods=["POST"])
def analyze_text():
    """
    Endpoint for analyzing text using the mental-roberta-base model.
    Accepts JSON with the format: {"text": "<your_text>"}
    """
    try:
        # Extract text from the incoming request
        data = request.json
        if "text" not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400

        text = data["text"]

        # Perform classification
        result = classification_pipeline(text)

        # Return the result as JSON
        return jsonify({
            "text": text,
            "analysis_result": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=8090)
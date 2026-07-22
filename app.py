from flask import Flask, render_template, request, jsonify
from utils.feature_extractor import FeatureExtractor
from utils.predictor import Predictor
from utils.validator import URLValidator

app = Flask(__name__)

extractor = FeatureExtractor()
predictor = Predictor()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    url = data.get("url")
    model_name = data.get("model", "xgboost")
        # Validate URL format
    if not URLValidator.is_valid_url(url):
        return jsonify({
            "error": "Please enter a valid URL (including https://)"
        })

    # Check if the domain actually exists
    if not URLValidator.domain_exists(url):
        return jsonify({
            "error": "This website does not exist."
        })

    # Extract features
    features = extractor.extract_features(url)

    # Predict
    result = predictor.predict(
        features,
        model_name=model_name
    )

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
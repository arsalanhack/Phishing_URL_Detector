from flask import Flask, render_template, request, jsonify

from utils.validator import validate_url
from utils.feature_extractor import FeatureExtractor
from utils.predictor import Predictor

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

    if not validate_url(url):
        return jsonify({
            "error": "Invalid URL"
        }), 400

    features = extractor.extract_features(url)


    result = predictor.predict(
        features,
        model_name=model_name
    )
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
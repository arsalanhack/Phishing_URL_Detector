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
    return jsonify({
    "prediction": result["prediction"],
    "confidence": result["confidence"],
    "model": result["model"],
    "features": {
        "having_IP_Address": features[0],
        "URL_Length": features[1],
        "having_At_Symbol": features[2],
        "double_slash_redirecting": features[3],
        "Prefix_Suffix": features[4],
        "having_Sub_Domain": features[5],
        "SSLfinal_State": features[6],
        "HTTPS_token": features[7],
        "Shortining_Service": features[8],
        "DNSRecord": features[9],
        "URL_of_Anchor": features[10]
    }
})


if __name__ == "__main__":
    app.run(debug=True)
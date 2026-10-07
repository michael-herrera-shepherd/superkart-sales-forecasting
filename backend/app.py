import joblib
import pandas as pd
from flask import Flask, request, jsonify

superkart_api = Flask("superkart_api")

# Load the trained sales forecasting pipeline (path is relative to the container's /app folder)
model = joblib.load("SuperKart_Model.joblib")

FEATURES = [
    "Product_Weight", "Product_Sugar_Content", "Product_Allocated_Area", "Product_MRP",
    "Store_Size", "Store_Location_City_Type", "Store_Type",
    "Product_Id_char", "Store_Age_Years", "Product_Type_Category",
]


@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Prediction API!"


@superkart_api.post("/v1/predict")
def predict_sales():
    data = request.get_json()
    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400
    input_data = pd.DataFrame([{f: data[f] for f in FEATURES}])
    prediction = float(model.predict(input_data)[0])
    return jsonify({"Sales": round(prediction, 2)})


if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=10000)

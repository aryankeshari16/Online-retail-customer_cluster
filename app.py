from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = joblib.load("kmeans_customer_segmentation.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predict():
    try:
        # Get input from form
        frequency = float(request.form['frequency'])
        monetary = float(request.form['monetary'])
        avg_order_value = float(request.form['aov'])
        avg_basket_size = float(request.form['basket'])

        # Prepare features
        features = np.array([[frequency, monetary, avg_order_value, avg_basket_size]])
        features_scaled = scaler.transform(features)

        # Predict cluster
        cluster = model.predict(features_scaled)[0]

        return render_template("index.html", prediction=f"Customer belongs to Cluster {cluster}")
    except Exception as e:
        return render_template("index.html", prediction=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

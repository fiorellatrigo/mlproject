from flask import Flask, request, render_template

from src.pipeline.predict_pipeline import PredictPipeline, CustomData

application = Flask(__name__)  # entry point for our flask app

app = application

# Route to render the home page


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == "GET":
        # Render the home page template for GET requests
        return render_template("home.html")

    data = CustomData(
        gender=request.form.get("gender"),
        race_ethnicity=request.form.get("race_ethnicity"),
        parental_level_of_education=request.form.get(
            "parental_level_of_education"
        ),
        lunch=request.form.get("lunch"),
        test_preparation_course=request.form.get("test_preparation_course"),
    )  # Create an instance of CustomData with the input features from the form

    # Convert the input features into a DataFrame for prediction
    pred_df = data.get_data_as_dataframe()
    # Create an instance of the PredictPipeline class to handle the prediction process
    predict_pipeline = PredictPipeline()
    # Use the PredictPipeline to make predictions based on the input features
    results = predict_pipeline.predict(features=pred_df)

    pred_class = int(results[0])  # Get the predicted class from the results
    # If the predicted class is 1, it indicates a high performer (above median score)
    if pred_class == 1:
        prediction_label = "High Performer (Above Median Score)"
        prediction_tier = "high"
    else:
        # If the predicted class is 0, it indicates an at-risk or standard performer (below median score)
        prediction_label = "At-Risk / Standard (Below Median Score)"
        prediction_tier = "standard"

    return render_template(
        "home.html",
        prediction=prediction_label,
        prediction_tier=prediction_tier,
    )  # Render the home page template with the prediction results and tier information


if __name__ == "__main__":
    # Run the Flask app on all available network interfaces with debug mode enabled
    app.run(host="0.0.0.0", debug=True)

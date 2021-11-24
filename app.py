from flask import Flask, render_template, request
import pickle
import pandas as pd

# Initialise the Flask app
app = Flask(__name__)

# Use pickle to load in the pre-trained model
filename = "models/model.sav"
model = pickle.load(open(filename, "rb"))

# Set up the main route
@app.route('/', methods=["GET", "POST"])
def main():

    if request.method == "POST":
        # Extract the input from the form
        PM2 = request.form.get("PM2.5")
        PM10 = request.form.get("PM10")
        NOx = request.form.get("NOx")

        # Create DataFrame based on input
        input_variables = pd.DataFrame([[PM2, PM10, NOx]],
                                       columns=['PM2.5', 'PM10', 'NOx'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        # Given that the prediction is stored in an array we simply extract by indexing
        prediction = model.predict(input_variables)[0]
    
        # We now pass on the input from the from and the prediction to the index page
        return render_template("main.html",
                                     original_input={'PM2.5':PM2,
                                                     'PM10':PM10,
                                                     'NOx':NOx},
                                     result=prediction
                                     )
    # If the request method is GET
    return render_template("main.html")

if __name__ == '__main__':
    app.run(debug=True)

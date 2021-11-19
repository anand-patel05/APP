import flask
import pickle
import pandas as pd

# Use pickle to load in the pre-trained model
with open(f'model/prediction_model_xgboost.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        PM3 = flask.request.form['PM2.5']
        PM10 = flask.request.form['PM10']
        NOx = flask.request.form['NOx']

        # Make DataFrame for model
        input_variables = pd.DataFrame([[PM3, PM10, NOx]],
                                       columns=['PM2.5', 'PM10', 'NOx'],
                                       dtype=float,
                                       index=['input'])

        # Get the model's prediction
        prediction = model.predict(input_variables)[0]
    
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.render_template('page1.html',
                                     original_input={'PM2.5':PM3,
                                                     'PM10':PM10,
                                                     'NOx':NOx},
                                     result=prediction,
                                     )
@app.route('/page1')
def page1():
    return flask.render_template('page1.html') 
   
@app.route('/page2')
def page2():
    return flask.render_template('page2.html') 

@app.route('/main')
def main():
    return flask.render_template('main.html') 


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify,  render_template

import joblib

app = Flask(__name__)

@app.route("/")
def index():
    '''
    returns a page
    '''
    print('in index.html')
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    '''
    predicts wine quality
    '''
    # Check if request has a JSON content
    if request.json:
        # Get the JSON as dictionnary
        req = request.get_json()
        # Check mandatory key
        if "input" in req.keys():
            #Transform input in dataframe
            # Load model
            classifier = joblib.load("models/model.joblib")
            # Predict
            prediction = classifier.predict(req['input'])
            # Return the result as JSON but first we need to transform the
            # result so as to be serializable by jsonify()
            #prediction = str(prediction[0])
            return jsonify([str(pred) for pred in prediction]), 200
    return jsonify({"msg": "Error: not a JSON or no email key in your request"})

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)

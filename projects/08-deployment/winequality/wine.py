from flask import Flask, request, jsonify,  render_template, url_for

import joblib

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    '''
    returns an index page
    '''
    print('///In index.html')
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    '''
    Rredicts wine quality
    '''
    #if request.form.get('action-predict') == 'Submit':
        #print('Button submit pressed')
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
    return jsonify({"msg": "Error: not a JSON or no input key in your request"})

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)

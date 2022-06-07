from flask import Flask, request, url_for, redirect, render_template
import pandas as pd
import numpy as np

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "AGB_2yx6Xgk4rJKsWsd5334VhDE9i4hB7I9yhor2YQMY"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def pred():
    inputFeatures = [float(x) for x in request.form.values()]
    featuresValue = [np.array(inputFeatures)]
    
    featureName = ['FULL_TIME_POSITION', 'PREVAILING_WAGE', 'YEAR','SOC_N']
    
    df = pd.DataFrame(featuresValue, columns=featureName)
    payload_scoring = {"input_data": [{"field": [["FULL_TIME_POSITION", "PREVAILING_WAGE","YEAR","SOC_N"]], "values": [inputFeatures]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/aa28338c-0107-4bcb-88a6-61577e133bfc/predictions?version=2022-06-03', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    pred=response_scoring.json()
    print(pred)
    output = pred['predictions'][0]['values'][0][0]
    print(output)
    
    return render_template('result.html', prediction_text = output)
        
if __name__ == '__main__':
    app.run(debug=True)

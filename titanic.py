from flask import Flask, request,jsonify
from sklearn.externals import joblib
import pandas as pd
import json
import urllib2


from flask import render_template
from flask import request
from flask import make_response

app = Flask(__name__)

DEFAULTS = {'Age': 32,
            'Sex': 'male',
            'Embarked': 'S'
            }

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    return DEFAULTS[key]

@app.route('/')
def home():
	Age = get_value_with_fallback("Age")
	Sex = get_value_with_fallback("Sex")
	Embarked = get_value_with_fallback("Embarked")
	json_ = {'Age':float(Age),'Sex':Sex,'Embarked':Embarked}
	query_df = pd.DataFrame(json_,index=[0])
	query = pd.get_dummies(query_df)
	for col in model_columns:
		if col not in query.columns:
			query[col]=0
	prediction = clf.predict(query)
	pred = prediction[0]

	response = make_response(render_template("home.html",Age=Age,Sex=Sex,Embarked=Embarked,pred=pred))
	return response



if __name__=='__main__':
	clf = joblib.load('model.pkl')
	model_columns = joblib.load('model_columns.pkl')
	app.run(port=8080)


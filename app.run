#/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, jsonify
import engine

import json
import sys
app = Flask(__name__)

print sys.argv
MODEL = "randomForest"
model = engine.Model()


@app.route('/{}'.format(MODEL), methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
		message = """Would you like to predict iris data ? Please type:
curl  -X POST -H "Content-Type: application/json" -d '[[0,0],[0,2]]' http://127.0.0.1:5000/randomForest
					"""
		return message
    elif request.method =='POST':
		try:
			prediction = model.predictor(request.get_json(force=True))
		except Exception,e:
			return str(e)+'\n'
		
			
    return jsonify(list(prediction))

if __name__ == '__main__':
    app.run()

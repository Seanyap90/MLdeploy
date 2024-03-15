from flask import Flask
from flask import Flask, jsonify, request, Response
from datetime import datetime, time
from flask_cors import CORS
from time import sleep
from model_manager import ModelManager
import os
import sys
from time import sleep
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from server import app
from server import load_model_startup

@app.route("/api/models", methods=['GET'])
def get_models():
    model_manager = ModelManager()
    models = model_manager.get_models()    
    return models

@app.route("/api/models/<qualified_name>/predict", methods=['POST'])
def predict(qualified_name):
    sleep(0.5)
    data = request.json
    sensor_num = data.get("SENSOR_NUM")
    time_value = data.get("TIME")
    dc_power_value = float(data.get("DC_POWER")) if data.get("DC_POWER") else None

    if time_value is None or dc_power_value is None:
        return jsonify({"error": "Please provide both TIME and DC_POWER values."}), 400
    
    # getting the model object from the Model Manager
    model_manager = ModelManager()
    model_object = model_manager.get_model(qualified_name=qualified_name)
    
    if model_object is None:
        response = dict(type="ERROR", message="Model not found.")
        return Response(jsonify(response), status=404, mimetype='application/json')
    
    try:
        print("predicting...")
        status = model_object.predict(data)
        status.update({'inverter_id': sensor_num})
        print(status)
        
        return jsonify(status), 200
        
    except Exception as e:
        response = dict(type="PREDICTION ERROR", message=str(e))
        return Response(jsonify(response), status=400, mimetype='application/json')

if __name__ == '__main__':
    load_model_startup()
    app.run(host='<YOUR-SERVER_IP>', port=5000, debug=True)

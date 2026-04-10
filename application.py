from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime
import json
import os

application = Flask(__name__)

app = application
# API Gateway endpoint for Lambda-2
API_GATEWAY_URL = "https://bnu6sz7h79.execute-api.us-east-1.amazonaws.com/default/lambda-store-fetch-alert-x24248789"

def fetch_sensor_data():
    """Fetch data from DynamoDB via Lambda-2"""
    try:
        response = requests.get(API_GATEWAY_URL)
        if response.status_code == 200:
            data = response.json()
            print(f"Fetched {len(data)} records")  # Debug log
            if len(data) > 0:
                print(f"Sample record: {data[0]}")  # Debug log to see field names
            # Sort by timestamp (newest first)
            data.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return data
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
    except Exception as e:
        print(f"Exception in fetch_sensor_data: {str(e)}")
        return []

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/sensor-data')
def get_sensor_data():
    """API endpoint to get latest sensor data"""
    data = fetch_sensor_data()
    return jsonify(data)

@app.route('/api/latest-reading')
def get_latest_reading():
    """Get the most recent sensor reading"""
    data = fetch_sensor_data()
    if data:
        return jsonify(data[0])
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
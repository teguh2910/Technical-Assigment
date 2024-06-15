from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://sensor_data_db:qwerty24@sicdb.o5iy0rc.mongodb.net/')  # Adjust the URI as needed
db = client['sensor_data_db']
collection = db['sensor_data']

@app.route('/sensor', methods=['POST'])
def sensor_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    # Insert data into MongoDB
    sensor_record = {
        'temperature': temperature,
        'humidity': humidity
    }
    result = collection.insert_one(sensor_record)
    
    if result.acknowledged:
        print(f"Inserted data - Temperature: {temperature} °C, Humidity: {humidity} %")
        return jsonify({"status": "success"}), 200
    else:
        print("Failed to insert data")
        return jsonify({"status": "failure"}), 500
    
@app.route('/sensor1/temperature/all', methods=['GET'])
def get_all_sensor_data():
    # Retrieve all temperature data
    data = list(collection.find({}, {'_id': 0, 'temperature': 1}))
    return jsonify(data), 200

@app.route('/sensor1/humidity/all', methods=['GET'])
def get_all_humidity_data():
    # Retrieve all humidity data
    data = list(collection.find({}, {'_id': 0, 'humidity': 1}))
    return jsonify(data), 200

@app.route('/sensor1/avg', methods=['GET'])
def get_avg_sensor_data():
    # Retrieve all data
    data = list(collection.find({}, {'_id': 0, 'temperature': 1, 'humidity': 1}))
    
    if not data:
        return jsonify({"error": "No data found"}), 404

    # Calculate average temperature and humidity
    total_temp = sum(d['temperature'] for d in data)
    total_humidity = sum(d['humidity'] for d in data)
    count = len(data)

    avg_temp = total_temp / count
    avg_humidity = total_humidity / count

    avg_data = {
        'average_temperature': avg_temp,
        'average_humidity': avg_humidity
    }
    return jsonify(avg_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)

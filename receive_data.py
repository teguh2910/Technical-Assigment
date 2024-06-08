from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sensor', methods=['POST'])
def sensor_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    print(f"Received data - Temperature: {temperature} °C, Humidity: {humidity} %")
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000)

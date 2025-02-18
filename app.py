from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Initialize GPS data with default location (Chennai)
gps_data = {"latitude": 13.323407, "longitude": 80.152771}

@app.route('/')
def index():
    return render_template('map.html', lat=gps_data['latitude'], lon=gps_data['longitude'])

@app.route('/update', methods=['GET'])
def update_location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if lat and lon:
        gps_data['latitude'] = float(lat)
        gps_data['longitude'] = float(lon)
        print(f"📍 GPS Updated: Latitude: {lat}, Longitude: {lon}")

    return "Location updated successfully"

@app.route('/current_location', methods=['GET'])
def current_location():
    print("currentlocation")
    print(jsonify(gps_data))
    return jsonify(gps_data)  # Returns the latest coordinates as JSON

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

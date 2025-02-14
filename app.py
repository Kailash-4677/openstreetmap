from flask import Flask, request, render_template

app = Flask(_name_)

# Initialize GPS data with default location (Chennai)
gps_data = {"latitude": 13.0827, "longitude": 80.2707}

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

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=5000)

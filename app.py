from flask import Flask, request, render_template, jsonify
import smtplib
from email.mime.text import MIMEText
from geopy.distance import geodesic

app = Flask(__name__)

# Initialize GPS data with default location (Chennai)
gps_data = {"latitude": 13.323407, "longitude": 80.152771}
previous_location = gps_data.copy() 

# Set distance threshold (in meters)
DISTANCE_THRESHOLD = 200  # Change as needed

# Email credentials (replace with your details)
EMAIL_SENDER = "24404.cs@rmkcet.ac.in"
EMAIL_PASSWORD = "opener kailash"
EMAIL_RECEIVER = "kailashcricketer7@gmail.com"

# Function to send an email alert
def send_email_alert(new_lat, new_lon, distance):
    subject = "🚨 GPS Location Alert!"
    body = f"New GPS Location Detected!\nLatitude: {new_lat}, Longitude: {new_lon}\nMoved: {distance:.2f} meters."
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Use Gmail SMTP
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("📧 Email sent successfully!")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

@app.route('/')
def index():
    return render_template('map.html', lat=gps_data['latitude'], lon=gps_data['longitude'])

@app.route('/update', methods=['GET'])
def update_location():
    global previous_location
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    new_location = (lat, lon)
    old_location = (previous_location["latitude"], previous_location["longitude"])

    # Calculate distance moved
    distance_moved = geodesic(old_location, new_location).meters

    if lat and lon:
        gps_data['latitude'] = float(lat)
        gps_data['longitude'] = float(lon)
        previous_location = gps_data.copy()
        print(f"📍 GPS Updated: Latitude: {lat}, Longitude: {lon}")

    # If moved more than threshold, send an alert
    if distance_moved > DISTANCE_THRESHOLD:
        send_email_alert(lat, lon, distance_moved)

    return "Location updated successfully"

@app.route('/current_location', methods=['GET'])
def current_location():
    print("currentlocation")
    print(jsonify(gps_data))
    return jsonify(gps_data)  # Returns the latest coordinates as JSON

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

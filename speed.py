import xml.etree.ElementTree as ET
from datetime import datetime

def parse_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # GPX namespace
    namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}

    points = []

    # Iterate through track points or waypoints
    for trkpt in root.findall('.//gpx:trkpt', namespace):
        lat = trkpt.get('lat')
        lon = trkpt.get('lon')
        time = trkpt.find('gpx:time', namespace)

        if time is not None:
            points.append({
                'latitude': float(lat),
                'longitude': float(lon),
                'time': datetime.fromisoformat(time.text.replace('Z', '+00:00'))  # Convert to datetime
            })

    return points

def find_stops_with_zero_speed(points):
    zero_speed_locations = []

    for i in range(1, len(points)):
        # Calculate time difference in seconds
        time_diff = (points[i]['time'] - points[i - 1]['time']).total_seconds()
        
        # Calculate distance in meters (Haversine formula can be used for more accuracy)
        lat1, lon1 = points[i - 1]['latitude'], points[i - 1]['longitude']
        lat2, lon2 = points[i]['latitude'], points[i]['longitude']
        
        # Simple distance calculation (not very accurate for long distances)
        distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 111000  # Approximate conversion to meters

        # Calculate speed (m/s)
        if time_diff > 0:
            speed = distance / time_diff
        else:
            speed = 0

        # Check if speed is zero
        if speed == 0:
            zero_speed_locations.append({
                'latitude': points[i]['latitude'],
                'longitude': points[i]['longitude'],
                'time': points[i]['time']
            })

    return zero_speed_locations

# Example usage
gpx_file_path = 'filename.gpx'
points = parse_gpx(gpx_file_path)
zero_speed_locations = find_stops_with_zero_speed(points)

for location in zero_speed_locations:
    print(f"Location: ({location['latitude']}, {location['longitude']}), Time: {location['time']}")


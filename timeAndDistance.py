import xml.etree.ElementTree as ET
from datetime import datetime
import math

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

def calculate_total_distance_and_time(points):
    total_distance = 0.0  # in meters
    total_time = 0.0  # in seconds

    for i in range(1, len(points)):
        # Calculate time difference in seconds
        time_diff = (points[i]['time'] - points[i - 1]['time']).total_seconds()
        
        # Calculate distance using Haversine formula
        lat1, lon1 = math.radians(points[i - 1]['latitude']), math.radians(points[i - 1]['longitude'])
        lat2, lon2 = math.radians(points[i]['latitude']), math.radians(points[i]['longitude'])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371e3  # Radius of Earth in meters
        distance = r * c  # Distance in meters

        # Update total distance and time
        total_distance += distance
        total_time += time_diff

    return total_distance / 1000, total_time  # Convert distance to kilometers

# Example usage
gpx_file_path = 'filename.gpx'
points = parse_gpx(gpx_file_path)
total_distance_km, total_time = calculate_total_distance_and_time(points)

# Convert total time from seconds to a more readable format
total_hours = total_time // 3600
total_minutes = (total_time % 3600) // 60
total_seconds = total_time % 60

print(f"Total Distance: {total_distance_km:.2f} kilometers")
print(f"Total Time: {int(total_hours)} hours, {int(total_minutes)} minutes, {int(total_seconds)} seconds")


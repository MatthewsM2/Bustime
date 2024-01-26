import xml.etree.ElementTree as ET

def parse_gpx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # GPX namespace
    namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}

    bus_stops = []

    # Iterate through waypoints
    for wpt in root.findall('gpx:wpt', namespace):
        name = wpt.find('gpx:name', namespace)
        time = wpt.find('gpx:time', namespace)
        lat = wpt.get('lat')
        lon = wpt.get('lon')

        if name is not None and time is not None:
            bus_stops.append({
                'name': name.text,
                'arrival_time': time.text,
                'coordinates': {
                    'latitude': lat,
                    'longitude': lon
                    }
                })

    return bus_stops

# Example usage
gpx_file_path = 'filename.gpx'
bus_stops_info = parse_gpx(gpx_file_path)


print(bus_stops_info)
#for stop in bus_stops_info:
#    print(f"Bus Stop: {stop['name']}, Arrival Time: {stop['arrival_time']}")


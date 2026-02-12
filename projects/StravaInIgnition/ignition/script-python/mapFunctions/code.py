def decode_polyline(polyline_str):
    """
    Decodes a Google encoded polyline string into a list of (latitude, longitude) tuples.
    """
    index = 0
    lat = 0
    lng = 0
    coordinates = []
    length = len(polyline_str)

    while index < length:
        shift = 0
        result = 0
        
        # Decode Latitude
        while True:
            byte = ord(polyline_str[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        dlat = ~(result >> 1) if (result & 1) else (result >> 1)
        lat += dlat

        shift = 0
        result = 0
        
        # Decode Longitude
        while True:
            byte = ord(polyline_str[index]) - 63
            index += 1
            result |= (byte & 0x1f) << shift
            shift += 5
            if byte < 0x20:
                break
        dlng = ~(result >> 1) if (result & 1) else (result >> 1)
        lng += dlng

        # Store as (lat, lng). Note: Ignition Map (GeoJSON) often wants [lng, lat]
        # Standard Google/Leaflet wants [lat, lng].
        # We divide by 100,000.0 because that is the precision of the encoding
        coordinates.append([lat / 100000.0, lng / 100000.0])

    return coordinates
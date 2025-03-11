import math



def get_center(coords):
    latitudes = [coords[0][0], coords[1][0], coords[2][0], coords[3][0]]
    longitudes = [coords[0][1], coords[1][1], coords[2][1], coords[3][1]]
    return sum(latitudes) / 4, sum(longitudes) / 4



def midpoint_gps(point1, point2):
    """
    Calculate the midpoint (center) between two GPS coordinates.

    :param point1: Tuple (lat1, lon1) in degrees (first point).
    :param point2: Tuple (lat2, lon2) in degrees (second point).
    :return: Tuple (mid_lat, mid_lon) in degrees (midpoint of the segment).
    """
    lat1, lon1 = map(math.radians, point1)  # Convert degrees to radians
    lat2, lon2 = map(math.radians, point2)

    # Compute the midpoint
    Bx = math.cos(lat2) * math.cos(lon2 - lon1)
    By = math.cos(lat2) * math.sin(lon2 - lon1)

    mid_lat = math.atan2(math.sin(lat1) + math.sin(lat2), math.sqrt((math.cos(lat1) + Bx) ** 2 + By ** 2))
    mid_lon = lon1 + math.atan2(By, math.cos(lat1) + Bx)

    # Convert back to degrees
    return (math.degrees(mid_lat), math.degrees(mid_lon))



def move_gps(initial_coord, distance, direction):
    """
    Move from an initial GPS coordinate (latitude, longitude) a certain distance in a given direction.

    :param initial_coord: Tuple (latitude, longitude) in degrees.
    :param distance: Distance to move in meters.
    :param direction: Angle in degrees (0° = North, 90° = East, 180° = South, 270° = West).
    :return: Tuple (new_lat, new_lon) in degrees.
    """
    R = 6371000  # Earth’s radius in meters
    lat0, lon0 = map(math.radians, initial_coord)  # Convert degrees to radians
    theta_rad = math.radians(direction)
    new_lat = lat0 + (distance / R) * math.cos(theta_rad)
    new_lon = lon0 + (distance / R) * math.sin(theta_rad) / math.cos(lat0)
    return (math.degrees(new_lat), math.degrees(new_lon))



def calculate_bearing(point1, point2):
    """
    Calculate the bearing (direction) from point1 to point2 in degrees.

    :param point1: Tuple (lat1, lon1) in degrees (initial GPS coordinate).
    :param point2: Tuple (lat2, lon2) in degrees (destination GPS coordinate).
    :return: Bearing in degrees (0° = North, 90° = East, 180° = South, 270° = West).
    """
    lat1, lon1 = map(math.radians, point1)  # Convert to radians
    lat2, lon2 = map(math.radians, point2)

    delta_lon = lon2 - lon1  # Difference in longitude

    # Calculate bearing using the formula
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)

    bearing_rad = math.atan2(x, y)  # Compute the arctangent
    bearing_deg = math.degrees(bearing_rad)  # Convert radians to degrees

    return (bearing_deg + 360) % 360  # Normalize to 0°–360°
import math
import os
import time

import folium
from selenium import webdriver


def get_center(coords):
    latitudes = [coords[0][0], coords[1][0], coords[2][0], coords[3][0]]
    longitudes = [coords[0][1], coords[1][1], coords[2][1], coords[3][1]]
    return sum(latitudes) / 4, sum(longitudes) / 4


def generate_map(coords, new_coords):
    center = get_center(coords)
    m = folium.Map(location=center, zoom_start=13)  # Zoom out to cover ~20km²
    folium.Polygon(coords, color="red", fill=True, fill_opacity=0.3).add_to(m)
    folium.Polygon(new_coords, color="blue", fill=False).add_to(m)

    map_path = os.path.abspath("map.html")
    m.save(map_path)
    print(f"Harta a fost generată și salvată ca '{map_path}'.")
    return map_path


def save_map_as_png(map_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1200x800')
    driver = webdriver.Chrome(options=options)

    driver.get("file://" + map_path)
    time.sleep(5)  # Așteptare pentru încărcarea completă a hărții
    screenshot_path = os.path.abspath("map.png")
    driver.save_screenshot(screenshot_path)
    driver.quit()
    print(f"Harta a fost salvată ca '{screenshot_path}'.")


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


if __name__ == "__main__":
    coords = []

    # for i in range(4):
    #     lat = float(input("Introdu latitudinea (xx.xx): "))
    #     long = float(input("Introdu longitudinea (xx.xx): "))
    #     coords.append((lat, long))

    coords.append((46.790371, 23.698120))
    coords.append((46.790871, 23.697970))  # 46.790834, 23.698013 [(46.79430091101429, 23.712094210326722)]
    coords.append((46.784788, 23.670933))  # stanga sus
    coords.append((46.784303, 23.671148))
    center = get_center(coords)

    angle = calculate_bearing(coords[1], coords[2])

    lat, long = move_gps(center, 2000, angle - 180)  # dreapta jos
    new_coords = [(lat, long)]
    lat, long = move_gps(center, 2000, angle)  # stanga jos
    new_coords.append((lat, long))

    new_center = move_gps(center, 1000, angle+90)
    lat, long = move_gps(new_center, 2000, angle)
    new_coords.append((lat, long))
    lat, long = move_gps(new_center, 2000, angle - 180)
    new_coords.append((lat, long))

    map_file = generate_map(coords, new_coords)
    save_map_as_png(map_file)

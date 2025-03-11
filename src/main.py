import os
import time
import folium
from selenium import webdriver

from src.gps_math import *


def compute_approach_coordinates(center, direction, length, width):
    coordinates = []

    lat, long = move_gps(center, length / 2, direction - 180)  # dreapta jos
    coordinates.append((lat, long))
    lat, long = move_gps(center, length / 2, direction)  # stanga jos
    coordinates.append((lat, long))

    new_center = move_gps(center, width, direction + 90)

    lat, long = move_gps(new_center, length / 2, direction)
    coordinates.append((lat, long))
    lat, long = move_gps(new_center, length / 2, direction - 180)
    coordinates.append((lat, long))

    coordinates.append(coordinates[0]) # for completing the polygon
    return coordinates



def draw_runway(coordinates, map):
    folium.Polygon(coordinates, color="red", fill=True, fill_opacity=0.3).add_to(map)

def draw_approach(coordinates, map):
    folium.PolyLine(coordinates, color="blue", fill=False).add_to(map)



def generate_map(runway_center, runway_coordinates, approach_coordinates):
    map = folium.Map(location=runway_center, zoom_start=13)
    draw_runway(runway_coordinates, map)
    draw_approach(approach_coordinates, map)

    map_path = os.path.abspath("../assets/map.html")
    map.save(map_path)
    print(f"Harta a fost generată și salvată ca '{map_path}'.")
    return map_path



def save_map_as_png(map_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1200x800')
    driver = webdriver.Chrome(options=options)

    driver.get("file://" + map_path)
    time.sleep(5)  # Așteptare pentru încărcarea completă a hărții
    screenshot_path = os.path.abspath("../assets/map.png")
    driver.save_screenshot(screenshot_path)
    driver.quit()
    print(f"Harta a fost salvată ca '{screenshot_path}'.")



def main():
    runway_coordinates = []

    # for i in range(4):
    #     lat = float(input("Introdu latitudinea (xx.xx): "))
    #     long = float(input("Introdu longitudinea (xx.xx): "))
    #     coords.append((lat, long))

    runway_coordinates.append((46.790371, 23.698120))  # dreapta sus
    runway_coordinates.append((46.790871, 23.697970))  # dreapta jos
    runway_coordinates.append((46.784788, 23.670933))  # stanga sus
    runway_coordinates.append((46.784303, 23.671148))  # stanga jos
    runway_coordinates.append((46.790371, 23.698120))  # dreapta sus dublu

    runway_center = get_center(runway_coordinates)
    direction = calculate_bearing(runway_coordinates[1], runway_coordinates[2])
    approach_length = 4000
    approach_width = 1000
    approach_coordinates = compute_approach_coordinates(runway_center, direction, approach_length, approach_width)

    map_file = generate_map(runway_center, runway_coordinates, approach_coordinates)
    save_map_as_png(map_file)





if __name__ == "__main__":
    main()
# example.py
import funcs as f
import cv2

# Specify paths
screenshot_path = 'img6.jpg'

image = f.open_resize(screenshot_path)

champion_images = f.get_champion_images(image)
hud_images = f.get_players_hud(image)
icons = f.load_icons("championIcons")
top_matches, list = f.find_best_matches(icons, champion_images)
print(list)
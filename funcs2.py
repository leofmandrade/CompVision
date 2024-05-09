
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import easyocr
import os

def read_and_preprocess_image(image_path, x, y, width, height):
    """Crop an image to a region of interest."""
    image = cv2.imread(image_path)
    cropped = image[y:y+height, x:x+width]
    return cropped

def extract_text_from_image(image):
    """Extract text from an image using EasyOCR."""
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image)
    return result[0][1] if result else ""

def parse_kda(text):
    """Parse KDA from text."""
    parts = text.replace(' ', '').split('/')
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    return "erro", "erro", "erro"

def clean_farm_text(text):
    """Clean farm text to handle character issues."""
    text = text.replace("O", "0").replace("o", "0")
    text = text.replace("S", "5").replace("s", "5")
    text = ''.join(filter(str.isdigit, text))
    return text

def compare_champions(image1, image2, threshold=0.8):
    """Compare two images to determine similarity."""
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    # Resize if necessary
    if image1_gray.shape != image2_gray.shape:
        image2_gray = cv2.resize(image2_gray, image1_gray.shape[::-1])

    # Calculate absolute differences and similarity
    difference = cv2.absdiff(image1_gray, image2_gray)
    similarity = 1 - np.mean(difference) / 255
    return similarity >= threshold

def get_kda_data(image_paths):
    """Retrieve KDA data for each player."""
    kda_data = []
    for path in image_paths:
        kda_text = extract_text_from_image(cv2.imread(path))
        kda_data.append(parse_kda(kda_text))
    return pd.DataFrame(kda_data, columns=["Kills", "Deaths", "Assists"])

def get_farm_data(image_paths):
    """Retrieve farm data for each player."""
    farm_data = []
    for path in image_paths:
        farm_text = extract_text_from_image(cv2.imread(path))
        farm_data.append(clean_farm_text(farm_text))
    return pd.DataFrame(farm_data, columns=["Farm"])

def identify_champions(champion_icons_folder, hud_images):
    """Identify champions using pixel-by-pixel comparison."""
    champion_icons = {f.split('.')[0]: cv2.imread(os.path.join(champion_icons_folder, f))
                      for f in os.listdir(champion_icons_folder)}

    champions = []
    for hud_image in hud_images:
        identified = "Unknown"
        for champion_name, icon in champion_icons.items():
            if compare_champions(icon, hud_image):
                identified = champion_name
                break
        champions.append(identified)

    return pd.DataFrame(champions, columns=["Champion"])

def get_data(screenshot_path, champion_icons_folder):
    """Extract all relevant data from a League of Legends screenshot."""
    # Coordinates and dimensions already calculated
    kda_coords = [(100, 100, 50, 30), (160, 100, 50, 30), (220, 100, 50, 30), (280, 100, 50, 30), (340, 100, 50, 30),(400, 100, 50, 30), (460, 100, 50, 30), (520, 100, 50, 30), (580, 100, 50, 30), (640, 100, 50, 30)]

    farm_coords = [(100, 140, 50, 30), (160, 140, 50, 30), (220, 140, 50, 30), (280, 140, 50, 30), (340, 140, 50, 30),(400, 140, 50, 30), (460, 140, 50, 30), (520, 140, 50, 30), (580, 140, 50, 30), (640, 140, 50, 30)]

    champion_coords = [(10, 10, 40, 40), (60, 10, 40, 40), (110, 10, 40, 40), (160, 10, 40, 40), (210, 10, 40, 40), (260, 10, 40, 40), (310, 10, 40, 40), (360, 10, 40, 40), (410, 10, 40, 40), (460, 10, 40, 40)]


    # Cropping regions and extracting text
    kda_images = [read_and_preprocess_image(screenshot_path, *coord) for coord in kda_coords]
    farm_images = [read_and_preprocess_image(screenshot_path, *coord) for coord in farm_coords]
    champion_images = [read_and_preprocess_image(screenshot_path, *coord) for coord in champion_coords]

    # Extract data
    kda_df = get_kda_data(kda_images)
    farm_df = get_farm_data(farm_images)
    champion_df = identify_champions(champion_icons_folder, champion_images)

    return pd.concat([champion_df, kda_df, farm_df], axis=1)




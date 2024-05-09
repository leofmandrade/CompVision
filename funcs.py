import cv2
import ctypes
import numpy as np
import os
import sys
#import pytesseract
import easyocr
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from scipy.stats import wasserstein_distance
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------------------------

def open_resize(path):
    image = cv2.imread(path)
    if image is not None:
        # Resize the image to match the screen resolution
        image = cv2.resize(image, (1300, 700))
    else:
        print("Error: Unable to load image")
    return image


def get_champion_images(image):
    xChampionIcon1, yChampionIcon1 = 20, 100
    xChampionIcon2, yChampionIcon2 = 20, 167
    xChampionIcon3, yChampionIcon3 = 20, 234
    xChampionIcon4, yChampionIcon4 = 20, 300
    xChampionIcon5, yChampionIcon5 = 20, 367
    xChampionIcon6, yChampionIcon6 = 1250, 100
    xChampionIcon7, yChampionIcon7 = 1250, 167
    xChampionIcon8, yChampionIcon8 = 1250, 234
    xChampionIcon9, yChampionIcon9 = 1250, 300
    xChampionIcon10, yChampionIcon10 = 1250, 367
    widthChampionIcon, heightChampionIcon = 30, 30
    championicon1 = image[yChampionIcon1:yChampionIcon1+heightChampionIcon, xChampionIcon1:xChampionIcon1+widthChampionIcon]
    championicon2 = image[yChampionIcon2:yChampionIcon2+heightChampionIcon, xChampionIcon2:xChampionIcon2+widthChampionIcon]
    championicon3 = image[yChampionIcon3:yChampionIcon3+heightChampionIcon, xChampionIcon3:xChampionIcon3+widthChampionIcon]
    championicon4 = image[yChampionIcon4:yChampionIcon4+heightChampionIcon, xChampionIcon4:xChampionIcon4+widthChampionIcon]
    championicon5 = image[yChampionIcon5:yChampionIcon5+heightChampionIcon, xChampionIcon5:xChampionIcon5+widthChampionIcon]
    championicon6 = image[yChampionIcon6:yChampionIcon6+heightChampionIcon, xChampionIcon6:xChampionIcon6+widthChampionIcon]
    championicon7 = image[yChampionIcon7:yChampionIcon7+heightChampionIcon, xChampionIcon7:xChampionIcon7+widthChampionIcon]
    championicon8 = image[yChampionIcon8:yChampionIcon8+heightChampionIcon, xChampionIcon8:xChampionIcon8+widthChampionIcon]
    championicon9 = image[yChampionIcon9:yChampionIcon9+heightChampionIcon, xChampionIcon9:xChampionIcon9+widthChampionIcon]
    championicon10 = image[yChampionIcon10:yChampionIcon10+heightChampionIcon, xChampionIcon10:xChampionIcon10+widthChampionIcon]
    champion_images = [["champ1",championicon1],["champ2",championicon2],["champ3",championicon3],["champ4",championicon4],["champ5",championicon5],["champ6",championicon6],["champ7",championicon7],["champ8",championicon8],["champ9",championicon9],["champ10",championicon10]] 
    return champion_images

def get_players_hud(image):
    widthChampionHud, heightChampionHud = 240, 29
    xChampionHud1, yChampionHud1 = 410, 550
    championHud1 = image[yChampionHud1:yChampionHud1+heightChampionHud, xChampionHud1:xChampionHud1+widthChampionHud]
    xChampionHud2, yChampionHud2 = 410, yChampionHud1 + heightChampionHud
    championHud2 = image[yChampionHud2:yChampionHud2+heightChampionHud, xChampionHud2:xChampionHud2+widthChampionHud]
    xChampionHud3, yChampionHud3 = 410, yChampionHud2 + heightChampionHud
    championHud3 = image[yChampionHud3:yChampionHud3+heightChampionHud, xChampionHud3:xChampionHud3+widthChampionHud]
    xChampionHud4, yChampionHud4 = 410, yChampionHud3 + heightChampionHud
    championHud4 = image[yChampionHud4:yChampionHud4+heightChampionHud, xChampionHud4:xChampionHud4+widthChampionHud]
    xChampionHud5, yChampionHud5 = 410, yChampionHud4 + heightChampionHud
    championHud5 = image[yChampionHud5:yChampionHud5+heightChampionHud, xChampionHud5:xChampionHud5+widthChampionHud]
    xChampionHud6, yChampionHud6 = 660, yChampionHud1
    championHud6 = image[yChampionHud6:yChampionHud6+heightChampionHud, xChampionHud6:xChampionHud6+widthChampionHud]
    xChampionHud7, yChampionHud7 = 660, yChampionHud6 + heightChampionHud
    championHud7 = image[yChampionHud7:yChampionHud7+heightChampionHud, xChampionHud7:xChampionHud7+widthChampionHud]
    xChampionHud8, yChampionHud8 = 660, yChampionHud7 + heightChampionHud
    championHud8 = image[yChampionHud8:yChampionHud8+heightChampionHud, xChampionHud8:xChampionHud8+widthChampionHud]
    xChampionHud9, yChampionHud9 = 660, yChampionHud8 + heightChampionHud
    championHud9 = image[yChampionHud9:yChampionHud9+heightChampionHud, xChampionHud9:xChampionHud9+widthChampionHud]
    xChampionHud10, yChampionHud10 = 660, yChampionHud9 + heightChampionHud
    championHud10 = image[yChampionHud10:yChampionHud10+heightChampionHud, xChampionHud10:xChampionHud10+widthChampionHud]
    championhudimages = [championHud1, championHud2, championHud3, championHud4, championHud5, championHud6, championHud7, championHud8, championHud9, championHud10]
    return championhudimages

def load_icons(icon_folder):
    icons = {}
    for filename in os.listdir(icon_folder):
        character_name = filename.split('.')[0]
        icon_path = os.path.join(icon_folder, filename)
        icon = cv2.imread(icon_path)
        icons[character_name] = icon
    return icons


def compare_images(image1, image2, region_size=20, tolerance=50):
    # Load and resize images

    image1 = cv2.resize(image1, (50, 50))
    image2 = cv2.resize(image2, (50, 50))

    # Aplica Gaussian Blur ao ícone do campeão
    image2 = cv2.GaussianBlur(image2, (5, 5), 0)

    # Compute full image difference with tolerance
    difference = cv2.absdiff(image1, image2)
    mask = difference > tolerance

    # Calculate full image matching percentage
    total_pixels = np.prod(difference.shape[:2])
    total_significant_differences = np.sum(mask)
    full_image_match_percentage = 100 - (total_significant_differences * 100 / total_pixels)

    # Calculate central region matching
    start = (50 - region_size) // 2
    end = start + region_size
    central_region1 = image1[start:end, start:end]
    central_region2 = image2[start:end, start:end]
    central_difference = cv2.absdiff(central_region1, central_region2)
    central_mask = central_difference > tolerance

    # Calculate central region matching percentage
    central_total_pixels = np.prod(central_difference.shape[:2])
    central_total_significant_differences = np.sum(central_mask)
    central_match_percentage = 100 - (central_total_significant_differences * 100 / central_total_pixels)

    return full_image_match_percentage, central_match_percentage, image1, image2, start, end

def find_best_matches(icons_images, champions_images):

    best_matches = {}
    top_matches = []
    # Compare each champion image with each icon
    for champ in champions_images:
        name = champ[0]
        image = champ[1]
        
        best_matches[name] = []
        for icon in icons_images.values():
            full_match, central_match, image1, image2, start, end = compare_images(image, icon)
            best_matches[name].append((full_match, central_match, champ, icon, image1, image2, start, end))

    for champ in champions_images:
        name = champ[0]
        image = champ[1]
        best_matches[name] = sorted(best_matches[name], key=lambda x: 0.3 * x[0] + 0.7 * x[1], reverse=True)
        top_matches.append(best_matches[name][0])   

    ordered_champion_list = []
    for match in top_matches:
        full_match, central_match, champ, icon, image1, image2, start, end = match
        key = [k for k, v in icons_images.items() if np.array_equal(v, icon)][0]
        ordered_champion_list.append(key)


    return top_matches, ordered_champion_list

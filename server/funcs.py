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

def crop_bounding_box(processed_image):
    # Find the bounding box
    non_zero_pixels = cv2.findNonZero(processed_image)
    x, y, w, h = cv2.boundingRect(non_zero_pixels)
    cropped = processed_image[y:y+h, x:x+w]
    return cropped

def image_processing(image):

    image = image.astype(np.float32) / 255.0
    # Increase the contrast of the image
    image = cv2.pow(image, 1.2)
    # Clip values to the range [0, 1]
    image = np.clip(image, 0, 1)
    # Convert back to 8-bits
    image = (255 * image).astype(np.uint8)
    image = cv2.resize(image, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC)
    # Raise brightness
    image = cv2.convertScaleAbs(image, alpha=1.1, beta=0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Use Otsu's method to automatically calculate the threshold value
    _, binary = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #binary = crop_bounding_box(binary)


   
    return binary

def limpaerrosgold(string):
    index =0
    for l in string:
        
        if l=='S':
            string = string[:index] + '5' + string[index+1:]
        if l=='O':
            string = string[:index] + '0' + string[index+1:]
        if l=='o':
            string = string[:index] + '0' + string[index+1:]
        if l=='s':
            string = string[:index] + '2' + string[index+1:]
        if l=='l':
            string = string[:index] + '1' + string[index+1:]
        if l=='Z':
            string = string[:index] + '2' + string[index+1:]
        if l=='k':
            string = string[:index] + string[index+1:]
        index+=1

    return string

def apaganaonumero(string):
    index =0
    for l in string:
        if l == '_':
            string.replace(l,'')
        if l == 'T':
            string = string[:index] + '1' + string[index+1:]
        elif (not (l.isdigit())) or (l=='<') or (l=='>'):
            string.strip(l)
        
            
        index+=1
    return string

def extract_text(image,reader):
    result = reader.readtext(image)
    try:
        text = result[0][1]
    except:
        try:
            image = crop_bounding_box(image)
            result = reader.readtext(image)
            text = result[0][1]
        except:
            text = "No text detected"
    return text


def get_top_bar(image,reader):
    xGold1, yGold1 = 749, 7
    widthGold, heightGold = 35, 22
    gold_roi1 = image[yGold1:yGold1+heightGold, xGold1:xGold1+widthGold]
    gold_roi1 = image_processing(gold_roi1)
    gold1 = extract_text(gold_roi1,reader)
    gold1 = limpaerrosgold(gold1)
    gold1 = apaganaonumero(gold1)
    gold1.replace('_','')
    

    
    #get gold_roi2
    xGold2, yGold2 = 543, 8
    gold_roi2 = image[yGold2:yGold2+heightGold, xGold2:xGold2+widthGold]
    gold_roi2 = image_processing(gold_roi2)
    gold2 = extract_text(gold_roi2,reader)
    gold2 = limpaerrosgold(gold2)
    gold2 = apaganaonumero(gold2)

    #get towers1
    xTowers1, yTowers1 = 797, 9
    widthTowers, heightTowers = 23, 19
    towers1 = image[yTowers1:yTowers1+heightTowers, xTowers1:xTowers1+widthTowers]
    towers1 = image_processing(towers1)
    towers1 = extract_text(towers1,reader)
    towers1 = apaganaonumero(towers1)

    #get towers2
    xTowers2, yTowers2 = 499, 9
    towers2 = image[yTowers2:yTowers2+heightTowers, xTowers2:xTowers2+widthTowers]
    towers2 = image_processing(towers2)
    towers2 = extract_text(towers2,reader)
    towers2 = apaganaonumero(towers2)

    #get dragons 1
    xDragons1, yDragons1 = 951, 0
    widthDragons, heightDragons = 25, 30
    dragons1 = image[yDragons1:yDragons1+heightDragons, xDragons1:xDragons1+widthDragons]
    dragons1 = image_processing(dragons1)
    dragons1 = extract_text(dragons1,reader)
    dragons1 = apaganaonumero(dragons1)

    #get dragons 2
    xDragons2, yDragons2 = 350, 0
    dragons2 = image[yDragons2:yDragons2+heightDragons, xDragons2:xDragons2+widthDragons]
    dragons2 = image_processing(dragons2)
    dragons2 = extract_text(dragons2,reader)
    dragons2 = apaganaonumero(dragons2)

    #get arauto 1
    xArauto1, yArauto1 = 899, 3
    widthArauto, heightArauto = 28, 25
    Arauto1 = image[yArauto1:yArauto1+heightArauto, xArauto1:xArauto1+widthArauto]
    Arauto1 = image_processing(Arauto1)
    arauto1 = extract_text(Arauto1,reader)
    arauto1 = apaganaonumero(arauto1)

    #get arauto 2
    xArauto2, yArauto2 = 401, 3
    Arauto2 = image[yArauto2:yArauto2+heightArauto, xArauto2:xArauto2+widthArauto]
    Arauto2 = image_processing(Arauto2)
    arauto2 = extract_text(Arauto2,reader)
    arauto2 = apaganaonumero(arauto2)

    #get larva1
    xLarva1, yLarva1 = 845, 9
    widthLarva, heightLarva = 15, 19
    larva1 = image[yLarva1:yLarva1+heightLarva, xLarva1:xLarva1+widthLarva]
    larva1 = image_processing(larva1)
    larva1 = extract_text(larva1,reader)
    larva1 = apaganaonumero(larva1)

    #get larva2
    xLarva2, yLarva2 = 449, 9
    larva2 = image[yLarva2:yLarva2+heightLarva, xLarva2:xLarva2+widthLarva]
    larva2 = image_processing(larva2)
    larva2 = extract_text(larva2,reader)
    larva2 = apaganaonumero(larva2)

    #get kills1
    xKills1, yKills1 = 667, 10
    widthKills, heightKills = 42, 27
    kills1 = image[yKills1:yKills1+heightKills, xKills1:xKills1+widthKills]
    kills1 = image_processing(kills1)
    kills1 = extract_text(kills1,reader)    
    kills1 = limpaerrosgold(apaganaonumero(kills1))

    #get kills2
    xKills2, yKills2 = 607, 10
    widthKills2, heightKills2 = 39, 30
    kills2 = image[yKills2:yKills2+heightKills2, xKills2:xKills2+widthKills2]
    kills2 = image_processing(kills2)
    kills2 = extract_text(kills2,reader)
    kills2 = limpaerrosgold(apaganaonumero(kills2))

    tabela = pd.DataFrame()
    tabela["TIME"] = ["RED", "BLUE"]
    tabela["GOLD"] = [gold1, gold2]
    tabela["TOWERS"] = [towers1, towers2]
    tabela["DRAGONS"] = [dragons1, dragons2]
    tabela["ARAUTO"] = [arauto1, arauto2]
    tabela["LARVA"] = [larva1, larva2]
    tabela["KILLS"] = [kills1, kills2]

    return tabela


def get_hud_info(hudimages,reader, championslist):
    lista1 = hudimages[:5]
    lista2 = hudimages[5:]
    listakda = []
    listafarm =[]

    xKDA, yKDA = 135, 10
    widthKDA, heightKDA = 50, 12

    xKDA2, yKDA2 = 60, 10
    widthKDA2, heightKDA2 = 50, 13

    xfarm, yfarm = 180, 10
    widthFarm, heightFarm = 34, 13

    xfarm2, yfarm2 = 25, 10
    widthFarm2, heightFarm2 = 34, 13

    for image in lista1:
        
        kda = image[yKDA:yKDA+heightKDA, xKDA:xKDA+widthKDA]
        kda = image_processing(kda)
        kda = extract_text(kda,reader)
        kda = limpaerrosgold(kda)
        kda = apaganaonumero(kda)
        if len(kda)==5:
            kda = kda[0] + '/' + kda[2] + '/' + kda[4]
        listakda.append(kda)

        farm = image[yfarm:yfarm+heightFarm, xfarm:xfarm+widthFarm]
        farm = image_processing(farm)
        farm = extract_text(farm,reader)
        farm = limpaerrosgold(farm)
        farm = apaganaonumero(farm)
        listafarm.append(farm)
    
    for image in lista2:
        kda = image[yKDA2:yKDA2+heightKDA2, xKDA2:xKDA2+widthKDA2]
        kda = image_processing(kda)
        kda = extract_text(kda,reader)
        if len(kda)==5:
            kda = kda[0] + '/' + kda[2] + '/' + kda[4]
        listakda.append(kda)

        farm = image[yfarm2:yfarm2+heightFarm2, xfarm2:xfarm2+widthFarm2]
        farm = image_processing(farm)
        farm = extract_text(farm,reader)
        listafarm.append(farm)

    tabelaplayer = pd.DataFrame()
    tabelaplayer["PLAYER"] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    tabelaplayer["TEAM"] = ["BLUE", "BLUE", "BLUE", "BLUE", "BLUE","RED", "RED", "RED", "RED", "RED"]
    kills = []
    deaths = []
    assists = []
    farm = []
    for kda in listakda:
        kda = kda.split('/')
        if len(kda)==3:
            kills.append(kda[0])
            deaths.append(kda[1])
            assists.append(kda[2])
        else:
            kills.append('erro')
            deaths.append('erro')
            assists.append('erro')
    
    for farm_text in listafarm:
        farm_text = farm_text.replace("O", "0")
        farm_text = farm_text.replace("o", "0")
        farm_text = farm_text.replace("S", "5")
        farm_text = farm_text.replace("s", "5")
        for l in farm_text:
            if not l.isdigit():
                farm_text = farm_text.replace(l, "")

        farm.append(farm_text)     
    
    tabelaplayer["KILLS"] = kills
    tabelaplayer["DEATHS"] = deaths
    tabelaplayer["ASSISTS"] = assists
    tabelaplayer["FARM"] = farm
    tabelaplayer["CHAMPION"] = championslist
    return tabelaplayer

def run(screenshot_path, icon_folder):
    image = open_resize(screenshot_path)
    champion_images = get_champion_images(image)
    hud_images = get_players_hud(image)
    icons = load_icons(icon_folder)
    top_matches, list = find_best_matches(icons, champion_images)
    reader = easyocr.Reader(['en'])
    df = get_top_bar(image, reader)
    df2 = get_hud_info(hud_images, reader, list)
    print(df2)
    print(df)








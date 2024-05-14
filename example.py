# example.py
import funcs as f
import cv2
import easyocr
import pandas as pd

# Specify paths
screenshot_path = 'img5.jpg'


icons = "championIcons"

f.run(screenshot_path, icons)


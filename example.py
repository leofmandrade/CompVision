# example.py
import funcs as f
import cv2
import easyocr
import pandas as pd

# Specify paths
screenshot_path = 'server/frames/frame_10500.jpg'


icons = "championIcons"

df, df2 = f.run(screenshot_path, icons)
print (df)


from PyPDF2 import PdfReader
from MusicScoreProc import *
import os
import cv2 as cv
from PIL import Image as ImagePIL

base_path = "C:\\Users\\Zhengjc\\Pictures\\Saved Pictures\\"
file_name = "Chopin_concerto_1_mvt1_HN-"


file_path= base_path+"Chopin Score pages\\30. Concerto No.1 2P HN Mvt 1\\"
current_loc = os.path.dirname(os.path.abspath(__file__))+"\\"
final_path = str(current_loc)+file_name+"\\"



for i in range(3, 10):
    save_path = file_path+file_name+str(i)+".png"
    print(save_path)
    img = cv.imread(save_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img[:] = cv.threshold(img, 127, 255, cv.THRESH_BINARY)[1]


    (img, W_Count, B_Count) = DespecklePatch(img, 10, 15)
    print("\tBlack/White Patches:", B_Count, W_Count)

    final_path = file_path+"SavePath\\"+file_name+str(i)+".png"
    cv.imwrite(final_path, img.astype(int),
               [cv.IMWRITE_PNG_BILEVEL, 1, cv.IMWRITE_PNG_COMPRESSION, 6])
    
    pimg = ImagePIL.open(final_path)
    pimg.save(save_path, dpi=(600.0, 600.0))
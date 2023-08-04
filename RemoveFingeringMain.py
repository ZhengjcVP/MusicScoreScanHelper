import math
import shutil
import time
from MusicScoreProc import *
from RemoveFingeringToolkit import *
import os
import cv2 as cv
from PIL import Image as ImagePIL

import ctypes
from win32api import GetSystemMetrics

start_time = time.time()

base_path="C:\\Users\\Zhengjc\\Pictures\\Saved Pictures\\"
file_path=base_path+"Chopin Score pages\\7. Prelude Wiener"

file_name="Chopin Prelude Wiener"

start_page=16
page_num=54

print("Folder Name: "+file_name)
print("\tProcessing from Page",str(start_page),"to",str(page_num-1))
print("\t",(page_num-start_page),"Pages Total.")
print("Loading PNG")

#Print adjusment made for each image
Verbose=True

count = 0

current_loc=os.path.dirname(os.path.abspath(__file__))+"\\"
temp_folder=file_name+"_Temp_RF\\"
temp_path=str(current_loc)+temp_folder
os.mkdir(temp_path)
final_path=str(current_loc)+file_name+"_RF\\"
os.mkdir(final_path)

# Pre-exist folder for matching templet. Currently not used.
template_path=str(current_loc)+file_name+"_RF_Number\\"

ctypes.windll.user32.SetProcessDPIAware()

ix=-1
iy=-1
Dragging=False
Scaling=0.3
ScreenW = GetSystemMetrics(0)
ScreenH = GetSystemMetrics(1)
Window_Name="Press Enter for Next Image"
# Proportion of window on screen. Must be <=1. 
# 1 is not recomended because the taskbar will cover part of image
Windows_Size=0.6

def readMouseInput(event, x, y, flags, param):
      
    global ix, iy, Dragging, img, prev_img, prev_img_2, Scaling
    
    RButton=False

    # Drag and hold left button to erase small objects
    if event == cv.EVENT_LBUTTONDOWN:
        if(Dragging==False):
            if(prev_img_2.any()):
                prev_img_2=prev_img.copy()
                prev_img=img.copy()
        Dragging = True
        ix = int(x/Scaling)
        iy = int(y/Scaling)
        showImageAndResize(img)

    elif event == cv.EVENT_MOUSEMOVE:
        if Dragging == True:
            ix = int(x/Scaling)
            iy = int(y/Scaling)
            if(img[iy, ix]==0):
                img=EraseNonConnected(img, ix, iy, area_thresh=500, brushsize=24)
                #time.sleep(0.05)
                showImageAndResize(img)

    # Right Mouse Button undo the last step
    elif event == cv.EVENT_RBUTTONDOWN:
        if(~RButton):
            RButton=True
            # print("Undo")
            img=prev_img.copy()
            prev_img=prev_img_2.copy()
            RButton=False
            showImageAndResize(img)

    elif event == cv.EVENT_LBUTTONUP:
        Dragging = False

    # Middle Button erases fingerings within line
    elif event == cv.EVENT_MBUTTONDOWN:
        ix = int(x/Scaling)
        iy = int(y/Scaling)
        prev_img_2=prev_img.copy()
        prev_img=img.copy()
        img=EraseConnected(img, ix, iy, brushsize=24)
        showImageAndResize(img)
        #time.sleep(0.05)

def showImageAndResize(img, isInMain=False):
    global Scaling
    H, W = img.shape[:2]
    Scaling=min(ScreenW/W, ScreenH/H)*Windows_Size
    img_TN=cv.resize(img, None, fx=Scaling, fy=Scaling, 
                     interpolation=cv.INTER_AREA)
    cv.imshow(Window_Name, img_TN)
    if(isInMain):
        if cv.waitKey(0)==27:
            return



for i in range(start_page, page_num):
    cur_name=file_name+"_"+str(i)+".png"
    shutil.copyfile(file_path + "\\" + cur_name, temp_path+cur_name)
    #os.system(cyp_cmd)
    #os.system("xcopy ")
#end for

print("\tLoading PNG Complete.")
print("Drag Left Button to erase.\nClick Right Button to undo.")
print("Click Middle Button to erase between lines")

for i in range(start_page, page_num):
    
    cur_name=file_name+"_"+str(i)+".png"
    img=cv.imread(temp_path+cur_name, cv.IMREAD_GRAYSCALE)
    img_original=cv.threshold(img, 127, 255, cv.THRESH_BINARY)[1]
    H, W = img.shape[:2]
    if(Verbose):
        print("Current IMG:", str(i))

    cv.namedWindow(Window_Name)
    cv.setMouseCallback(Window_Name, readMouseInput)

    # Obtain the cutoff position for upper and lower part
    min_pos=np.argmin(np.sum(255-img_original[(4*H//10):(6*H//10), :], axis=1))
    # Upper Part
    img=img_original[0:((4*H//10)+min_pos), :]

    prev_img=img.copy()
    prev_img_2=img.copy()

    #while True:
    #    img_TN=cv.resize(img, None, fx=Scaling, fy=Scaling,
    #                      interpolation=cv.INTER_AREA)
    #    cv.imshow(Window_Name, img_TN)
    #    if cv.waitKey(10) == 27:
    #        break
    showImageAndResize(img, True)
    cv.destroyAllWindows()

    print("Processing Lower")
    img_upper=img.copy()
    
    # Lower Part
    cv.namedWindow(Window_Name)
    cv.setMouseCallback(Window_Name, 
                         readMouseInput)
    img=img_original[((4*H//10)+min_pos+1):H-1, :]

    prev_img=img.copy()
    prev_img_2=img.copy()

    #while True:
    #    img_TN=cv.resize(img, None, fx=Scaling, fy=Scaling, 
    #                     interpolation=cv.INTER_AREA)
    #    cv.imshow(Window_Name, img_TN)
    #    if cv.waitKey(10) == 27:
    #        break
    showImageAndResize(img, True)
    cv.destroyAllWindows()

    img=cv.threshold(img, 127, 255, cv.THRESH_BINARY)[1]

    # Combine upper and lower files
    img=np.vstack((img_upper, img))
    # All done. Save file
    save_path=final_path+file_name+"_"+str(i)+".png"
    cv.imwrite(save_path, img.astype(int),
               [cv.IMWRITE_PNG_BILEVEL, 1, cv.IMWRITE_PNG_COMPRESSION, 6])
    save_path=final_path+file_name+"_mask_"+str(i)+".png"
    # mask=GenerateEraseMask(img)
    # cv.imwrite(save_path, mask.astype(int),
    #           [cv.IMWRITE_PNG_BILEVEL, 1, cv.IMWRITE_PNG_COMPRESSION, 6])
    # Change DPI. OpenCV doens't have this function, so use PIL
    pimg=ImagePIL.open(save_path)
    pimg.save(save_path, dpi=(600.0, 600.0))
end_time=time.time()
elapsed_time = int(end_time-start_time)
print("All Images Processed!\nTotal Time Cosumed:")
print(elapsed_time//60, "Minutes,", elapsed_time%60, "Seconds")
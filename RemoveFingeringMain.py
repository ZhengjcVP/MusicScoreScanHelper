import math
import shutil
import time
from MusicScoreProc import *
from RemoveFingeringToolkit import *
import os
import cv2 as cv
from PIL import Image as ImagePIL

start_time = time.time()

base_path="C:\\Users\\Zhengjc\\Pictures\\Saved Pictures\\"
file_path=base_path+"Chopin Score pages\\2. Chopin Etudes Op.10 Henle\\Despeckled"

file_name="Chopin Etudes Op 10 Henle"

start_page=24
page_num=26

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

ix=-1
iy=-1
Dragging=False

def readMouseInput(event, x, y, flags, param):
      
    global ix, iy, Dragging, img, prev_img, prev_img_2
    
    RButton=False

    # Drag and hold left button to erase small objects
    if event == cv.EVENT_LBUTTONDOWN:
        if(Dragging==False):
            if(prev_img_2.any()):
                prev_img_2=prev_img.copy()
                prev_img=img.copy()
        Dragging = True
        ix = x
        iy = y

    elif event == cv.EVENT_MOUSEMOVE:
        if Dragging == True:
            ix = x
            iy = y
            if(img[iy, ix]==0):
                img=EraseNonConnected(img, ix, iy, area_thresh=350, brushsize=16)
                #time.sleep(0.05)

    # Right Mouse Button undo the last step
    elif event == cv.EVENT_RBUTTONDOWN:
        if(~RButton):
            RButton=True
            # print("Undo")
            img=prev_img.copy()
            prev_img=prev_img_2.copy()
            RButton=False

    elif event == cv.EVENT_LBUTTONUP:
        Dragging = False

    # Middle Button erases fingerings within line
    elif event == cv.EVENT_MBUTTONDOWN:
        ix = x
        iy = y
        prev_img_2=prev_img.copy()
        prev_img=img.copy()
        img=EraseConnected(img, ix, iy, brushsize=16)
        #time.sleep(0.05)

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

    cv.namedWindow("Press Esc for next img")
    cv.setMouseCallback("Press Esc for next img", 
                         readMouseInput)

    min_pos=np.argmin(np.sum(255-img_original[(4*H//10):(6*H//10), :], axis=1))
    # Upper Part
    img=img_original[0:((4*H//10)+min_pos), :]
    img_before_erase=cv.resize(img, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
    img_before_erase=cv.threshold(img_before_erase, 127, 255, cv.THRESH_BINARY)[1]

    img=img_before_erase.copy()
    prev_img=img.copy()
    prev_img_2=img.copy()

    while True:
        cv.imshow("Press Esc for next img", img)
        if cv.waitKey(10) == 27:
            break
    cv.destroyAllWindows()

    img_erase_part_1=cv.bitwise_xor(img_before_erase, img)
    
    # Lower Part
    cv.namedWindow("Press Esc for next img")
    cv.setMouseCallback("Press Esc for next img", 
                         readMouseInput)
    img=img_original[((4*H//10)+min_pos+1):H-1, :]
    img_before_erase=cv.resize(img, None, fx=0.5, fy=0.5)
    img_before_erase=cv.threshold(img_before_erase, 127, 255, cv.THRESH_BINARY)[1]

    img=img_before_erase.copy()
    prev_img=img.copy()
    prev_img_2=img.copy()

    while True:
        cv.imshow("Press Esc for next img", img)
        if cv.waitKey(10) == 27:
            break
    cv.destroyAllWindows()

    img_erase_part_2=cv.bitwise_xor(img_before_erase, img)

    # Combine upper and lower part.
    # Then apply the erased part to original img
    img_erase=np.vstack((img_erase_part_1, img_erase_part_2))
    img_erase=cv.resize(img_erase, (W, H))

    # Adding a Threshold can reduce speckle on the final image
    img_erase=cv.threshold(img_erase, 80, 255, cv.THRESH_BINARY)[1]
    img=cv.bitwise_or(img_original, img_erase)

    img=cv.threshold(img, 127, 255, cv.THRESH_BINARY)[1]
    # Despeckle again because scaling will not cover all pixels
    (img, W_Count,B_Count)=DespecklePatch(img, 5, 10)
    if(Verbose):
        print("\tBlack/White Patches:", B_Count,W_Count)


    #All done. Save file
    save_path=final_path+file_name+"_"+str(i)+".png"
    cv.imwrite(save_path, img.astype(int),
               [cv.IMWRITE_PNG_BILEVEL, 1, cv.IMWRITE_PNG_COMPRESSION, 6])

    #Change DPI. OpenCV doens't have this function, so use PIL
    pimg=ImagePIL.open(save_path)
    pimg.save(save_path, dpi=(600.0, 600.0))
end_time=time.time()
elapsed_time = int(end_time-start_time)
print("All Images Processed!\nTotal Time Cosumed:")
print(elapsed_time//60, "Minutes,", elapsed_time%60, "Seconds")
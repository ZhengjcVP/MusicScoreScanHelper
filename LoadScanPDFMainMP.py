import math
import time
from PyPDF2 import PdfReader
from MusicScoreProc import *
import os
import cv2 as cv
from PIL import Image as ImagePIL
import multiprocessing 


def MPProcessImg(i, Verbose, temp_path, file_name, final_path, Tgt_W, Tgt_H, SCL, Filter_Thresh, Step_Size, UseStrongEnhance):
    #Rotate
    img=cv.imread(temp_path+file_name+"_"+str(i)+".jpg")
    img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    if(Verbose):
        print("Current IMG:", str(i))
    (img[:],rot_angle)=RotateByStraightLine(img,2,1440)
    if(Verbose):
        print("\tAngle:", rot_angle)

    #Crop
    (img, x0, x1, y0, y1)=CropWhite(img,Tgt_H, Tgt_W, 240, 120, 10)
    if(Verbose):
        print("\tCrop Edge:", x0, x1, y0, y1)

    #Resize
    img = cv.resize(img, (int(img.shape[1]*SCL),
                        int(img.shape[0]*SCL)), interpolation = cv.INTER_CUBIC)

    # Thresholding. 160 by default
    # Strong Enhance can only provide limited support to partially blurry scans
    if(UseStrongEnhance):
        img_strong=cv.threshold(img, Filter_Thresh+40,
                                 255, cv.THRESH_BINARY)[1]
        img[:]=cv.threshold(img, Filter_Thresh, 255, cv.THRESH_BINARY)[1]

        img_strong[:]=DespecklePatch(img_strong, 5, 50)[0]

        img=cv.bitwise_and(img, img_strong)
    else:
        img[:]=cv.threshold(img, Filter_Thresh, 255, cv.THRESH_BINARY)[1]

    #Despeckle.
    (img[:], W_Count,B_Count)=DespecklePatch(img, 5, 10)
    if(Verbose):
        print("\tBlack/White Patches:", B_Count,W_Count)

    # Fit the image to the given canvas size.
    # May pad or crop edges. Avoid cropping black parts.
    img=FitToCanvas(img,Tgt_W, Tgt_H, 10)

    # Centering
    # Divide the 2 edges into n part. 
    # Check the thumbnail (black or white) of the resulting nxn matrix.
    # Center the black part as possible.
    # Parts that an edge is divided into
    (img[:], LROffset, TBOffset)=CenterImg(img, 100, 280, 0)
    if(Verbose):
        print("\tFinal Offset:",LROffset, TBOffset)
    #All done. Save file
    save_path=final_path+file_name+"_"+str(i)+".png"
    cv.imwrite(save_path, img.astype(int),
               [cv.IMWRITE_PNG_BILEVEL, 1, cv.IMWRITE_PNG_COMPRESSION, 6])

    #Change DPI. OpenCV doens't have this function, so use PIL
    pimg=ImagePIL.open(save_path)
    pimg.save(save_path, dpi=(600.0, 600.0))

if __name__ == '__main__':
    start_time = time.time()

    base_path="C:\\Users\\Zhengjc\\Pictures\\Saved Pictures\\"
    #file_path=base_path+"Chopin Score pages\\7. Chopin Prelude Paderewski\\Chopin_prelude_paderewski.pdf"
    #file_path=base_path+"Chopin Score pages\\1. Chopin Ballades (New)\\Chopin_ballades_20230103.pdf"
    file_path=base_path+"Other Composer\\Schubert Sonata Wiener\\Schubert_D571_784_wiener_urtext.pdf"
    reader = PdfReader(file_path)
    file_name="Schubert D784"

    page=reader.pages[0]
    start_page=5
    page_num=100
    page_num=min(page_num, len(reader.pages))

    print("File Name:"+file_name)
    print("\tProcessing from Page",str(start_page),"to",str(page_num-1))
    print("\t",(page_num-start_page),"Pages Total.")

    #Print adjusment made for each image
    Verbose=True

    count = 0

    print("Loading PDF")
    current_loc=os.path.dirname(os.path.abspath(__file__))+"\\"
    temp_folder=file_name+"_Temp\\"
    temp_path=str(current_loc)+temp_folder
    os.mkdir(temp_path)
    final_path=str(current_loc)+file_name+"\\"
    os.mkdir(final_path)

    # One Image per page
    for i in range(page_num):
        for image_file_object in page.images:
            with open(str(count) + image_file_object.name, "wb") as fp:
                fp.write(image_file_object.data)
                count += 1
            os.rename(current_loc+str(i)+image_file_object.name, 
                          temp_path+file_name+"_"+str(i)+".jpg")
        #end for
        if (count < page_num):
            page=reader.pages[count]
    #end for

    print("\tLoading PDF Complete.")

    # Default A4 (or similar) under 600dpi: 4000x5400, 0.77
    # Change this if you are scanning under different DPI or page size
    Default_A4=True
    if(Default_A4):
        Tgt_W=4000
        Tgt_H=5400
        SCL=0.77
        Filter_Thresh=160
    else:
        Tgt_W=6000
        Tgt_H=8100
        SCL=1.155
        Filter_Thresh=160

    # Step Size for crop line. Smaller step size may capture more unwanted dusts,
    # while large step size may miss actual content
    Step_Size=10

    # Generate a stronger image (Higher Thershold)
    # Then combine with the original image with bitwise and
    # Can provide limited support to partially blurry scans
    # Not recomended for clean scans
    UseStrongEnhance=False
    processes=[]
    for i in range(start_page, page_num):
        p = multiprocessing.Process(target=MPProcessImg, args=(i, Verbose, temp_path, file_name, final_path, Tgt_W, Tgt_H, 
                                                               SCL, Filter_Thresh, Step_Size, UseStrongEnhance,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    end_time=time.time()
    elapsed_time = int(end_time-start_time)
    print("All Images Processed!\nTotal Time Cosumed:")
    print(elapsed_time//60, "Minutes,", elapsed_time%60, "Seconds" )
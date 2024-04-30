import math
import time

from PyPDF2 import PdfReader
from MusicScoreProc import *
import os
import cv2 as cv
from PIL import Image as ImagePIL

start_time = time.time()

base_path = "C:\\Users\\Zhengjc\\Pictures\\Saved Pictures\\"
#file_path=base_path+"Chopin Score pages\\7. Chopin Prelude Paderewski\\Chopin_prelude_paderewski.pdf"
file_path= base_path+"Beethoven sonata\\Op120 Diabelli\\Beethoven_op_120_diabelli.pdf"
if (not os.path.isfile(file_path)):
    print("======================")
    print("\tInput PDF does not exist.")
    print("\t Please check the file:\n\t"+file_path)
    print("======================")
    raise ValueError('Input PDF does not exist.')
reader = PdfReader(file_path)
file_name = "Op120 Diabelli"

page = reader.pages[0]
# -1 = No rotation
#  0 = Default rotation 
#  1 = Auto
#  2 = Text rotation (slower)
RotationMode = 0

start_page = 34
page_num = 64
page_num = min(page_num, len(reader.pages))

Use_start_end = True

page_range = []
if (Use_start_end):
    page_range = range(start_page, page_num)
else:
    # Customize page number here.
    page_range = [1, 23, 24]

    # Change start and end, for detecting input file
    start_page = page_range[0]
    page_num = page_range[-1]

print("File Name:"+file_name)
print("\tProcessing from Page", str(start_page), "to", str(page_num-1))
print("\t", (page_num-start_page), "Pages Total.")

# Print adjusment made for each image
Verbose = True

count = 0

print("Loading PDF")
current_loc = os.path.dirname(os.path.abspath(__file__))+"\\"
temp_folder = file_name+"_Temp\\"
temp_path = str(current_loc)+temp_folder
PDF_Loaded = False
if (os.path.exists(temp_path)):
    first_img_path = temp_path+file_name+"_"+str(start_page)+".jpg"
    last_img_path = temp_path+file_name+"_"+str(page_num-1)+".jpg"
    # Case: Folder exists, First and last file exist.
    # We assume we have all files needed.
    if(os.path.exists(first_img_path) and os.path.exists(last_img_path)):
        print("\tPDF Already loaded")
        PDF_Loaded = True
    # Folder exists, but is empty.
    elif (len(os.listdir(temp_path)) == 0):
        print("\tTemp folder exists, is empty")
    
    # Folder exists, is not empty, but does not contain all files we need.
    else:
        print("======================")
        print("\tTemp Image folder exists, but does not contain all files needed.")
        print("\t Please check the folder:\n\t"+temp_path)
        print("======================")
        raise ValueError('Temp Image folder corrupted.')

else:
    os.mkdir(temp_path)
final_path = str(current_loc)+file_name+"\\"
if (os.path.exists(final_path)):
    # Output path exists, but contains nothing.
    if (len(os.listdir(final_path)) == 0):
        print("\tOutput folder exists, is empty")
    else:
        print("======================")
        print("\tOutput folder exists and contains file(s).")
        print("\t Please check the folder:\n\t"+final_path)
        print("======================")
        raise ValueError('Output image folder contains files.')
else:
    os.mkdir(final_path)

# One Image per page
def readPDF():
    global reader, page, page_num, count, temp_path, final_path
    for i in range(page_num):
          for image_file_object in page.images:
              with open(str(count) + image_file_object.name, "wb") as fp:
                  fp.write(image_file_object.data)
                  count += 1
              os.rename(current_loc+str(i)+image_file_object.name,
                        temp_path+file_name+"_"+str(i)+".jpg")
          # end for
          if (count < page_num):
              page = reader.pages[count]
    # end for

if(not PDF_Loaded):
   readPDF()

print("\tLoading PDF Complete.")

# A4 (or similar): 4000x5400, 0.77. For most piano and orchestral pieces
# Default 3 to 4: 4500x6000, 0.8. For some orchestral and some very large piano pieces.
# HiRes 3 to 4: everything x1.5 from default 3 to 4
Default_A4 = False
Default_3to4 = True
HiRes_3to4 = False

# Change this if you are scanning under different DPI or page size
inDPI = 600
if (Default_A4):
    Tgt_W = 4000
    Tgt_H = 5400
    DPIRatio = 600/inDPI
    SCL = 0.77*DPIRatio
    Filter_Thresh = 160
    outDPI = 600.00
    dspBlackAmt = 2 #18
    dspWhiteAmt = 16 #10
elif (Default_3to4):
    Tgt_W = 4500
    Tgt_H = 6000
    DPIRatio = 600/inDPI
    SCL = DPIRatio*0.8
    Filter_Thresh = 180
    outDPI = 600.00
    dspBlackAmt = 18
    dspWhiteAmt = 9
elif (HiRes_3to4):
    Tgt_W = 6750
    Tgt_H = 9000
    DPIRatio = 600/inDPI
    SCL = DPIRatio*1.2
    Filter_Thresh = 170
    outDPI = 900.00 
    dspBlackAmt = 20
    dspWhiteAmt = 10
else:
    Tgt_W = 6750
    Tgt_H = 9000
    DPIRatio = 600/inDPI
    SCL = DPIRatio*1.0
    Filter_Thresh = 160
    outDPI = 600.00 
    dspBlackAmt = 0
    dspWhiteAmt = 0
# Filp or rotate page
Odd_page_flip = False
Even_page_flip = False

# Crop this amount (pixels) before using the CropWhite() command
# set to 0 for no cropping
PreCrop_Amt = 0
DoCrop = True

# Customize pre-cropping for 
Custom_PreCrop = True
# If true, even page will have precrop LR reversed.
Even_page_reverse_precrop = True
PreCrop_T = 180
PreCrop_L = 240
PreCrop_B = 80
PreCrop_R = 15

# Step Size for crop line. Smaller step size may capture more unwanted dusts,
# while large step size may miss actual content
Step_Size = 10

# Generate a stronger image (Higher Thershold)
# Then combine with the original image with bitwise and
# Can provide limited support to partially blurry scans
# Not recomended for clean scans
UseStrongEnhance = False
Use2LvFilter = False
SE_Thresh = 230
def printParams():
    print("Parameters:")
    print("\tDefault_A4:", Default_A4)
    if(not Default_A4):
        print("\tTgt_W:", Tgt_W, "Tgt_H:", Tgt_H, "SCL:", SCL)
    print("\tFilter_Thresh:", Filter_Thresh)
    if(Odd_page_flip):
        print("\tOdd_page_flip")
    if(Even_page_flip):
        print("\tOdd_page_flip")
    if(Custom_PreCrop):
        print("\tCustomized Pre Cropping LR TB:\n\t",
              PreCrop_T, PreCrop_B, PreCrop_L, PreCrop_R)
    elif(PreCrop_Amt != 0):
        print("\tPreCrop_Amt:", PreCrop_Amt)
    print("\tUseStrongEnhance:", UseStrongEnhance)


printParams()
#file_name1="mozart_sonata_wiener_smph_book1_Page_"
#file_name2="_Image_0001.jpg"
for i in page_range:

    # Alternative read file
    # if(i<=9):
    #     img = cv.imread(temp_path+file_name1+"00"+str(i)+file_name2)
    # elif(i<=99):
    #     img = cv.imread(temp_path+file_name1+"0"+str(i)+file_name2)
    # else:
    #     img = cv.imread(temp_path+file_name1+str(i)+file_name2)


    # Read File
    img = cv.imread(temp_path+file_name+"_"+str(i)+".jpg")
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if (Verbose):
        print("Current IMG:", str(i))
    
    # Image Height and Width
    img_W = img.shape[:2][0]
    img_H = img.shape[:2][1]

    # Flip horizontal then vertical. Equivalent to 180deg rotate.
    if ((Odd_page_flip and i % 2 == 1) or (Even_page_flip and i % 2 == 0)):
        if (Verbose):
            print("\tRotated 180 degrees")
        img = cv.flip(img, 0)
        img = cv.flip(img, 1)

    # Rotate
    if(RotationMode != -1):
        (img[:], rot_angle) = RotateByStraightLine(img, 2, 1440, RotationMode)
        if (Verbose):
            print("\tAngle:", rot_angle)
#
    # Crop before proceeding
    if(Custom_PreCrop):
        # Even page will have reflected precrop from odd page
        if (Even_page_reverse_precrop and i % 2 == 0):
            img = img[PreCrop_T:(img_W-PreCrop_B), 
                      PreCrop_R:(img_H-PreCrop_L)]
        # Normal Precrop for every page
        else:
            img = img[PreCrop_T:(img_W-PreCrop_B), 
                      PreCrop_L:(img_H-PreCrop_R)]
    elif(PreCrop_Amt != 0):
        img = img[PreCrop_Amt:(img_W-PreCrop_Amt), 
              PreCrop_Amt:(img_H-PreCrop_Amt)]

    # Re-calculate height and width after pre cropping.    
    img_W = img.shape[:2][0]
    img_H = img.shape[:2][1]

    # Crop
    if(DoCrop):
        (img, x0, x1, y0, y1) = CropWhite(img, Tgt_H, Tgt_W, 200, 120, 10)
        if (Verbose):
            print("\tCrop Edge:", x0, x1, y0, y1)
    # x0=0
    # y0=0
    # x1=min(6999, img_W) 
    # y1=min(5399, img_H)
    # img = img[0:x1, 0:y1]


    # Resize
    New_H = int(img.shape[1]*SCL)
    New_W = int(img.shape[0]*SCL)
    img = cv.resize(img, (New_H, New_W), interpolation=cv.INTER_CUBIC)

    # Thresholding. 160 by default
    # Strong Enhance can only provide limited support to partially blurry scans
    if (UseStrongEnhance):
        img = StrongEnhance(img, Filter_Thresh, SE_Thresh, 80)
    elif (Use2LvFilter):
        img = TwoLvFilter(img, Filter_Thresh, SE_Thresh, dspBlackAmt, dspWhiteAmt, True)
    else:
        img[:] = cv.threshold(img, Filter_Thresh, 255, cv.THRESH_BINARY)[1]

    # Despeckle.
    if(not Use2LvFilter):
        (img[:], W_Count, B_Count) = DespecklePatch(img, dspWhiteAmt, dspBlackAmt)
        if (Verbose):
            print("\tBlack/White Patches:", B_Count, W_Count)

    # Fit the image to the given canvas size.
    # May pad or crop edges. Avoid cropping black parts.
    img = FitToCanvas(img, Tgt_W, Tgt_H, 10)

    # Centering
    (img[:], LROffset, TBOffset) = CenterImg(img, 100, 280, 0)
    if (Verbose):
        print("\tFinal Offset:", LROffset, TBOffset)

    # All done. Save file
    save_path = final_path+file_name+"_"+str(i)+".png"
    cv.imwrite(save_path, img.astype(int),
               [cv.IMWRITE_PNG_BILEVEL, 1, cv.IMWRITE_PNG_COMPRESSION, 6])

    # Change DPI. OpenCV doens't have this function, so use PIL
    pimg = ImagePIL.open(save_path)
    pimg.save(save_path, dpi=(outDPI, outDPI))
# end for i in range

end_time = time.time()
elapsed_time = int(end_time-start_time)
print("All Images Processed!\nTotal Time Cosumed:")
print(elapsed_time//60, "Minutes,", elapsed_time % 60, "Seconds")

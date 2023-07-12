import cv2 as cv
import numpy as np
import math

# Rotate arrcording to angle of horizontal line.
# Should not exceed +- 5 degrees
# start_resolution and angle_percision are params of the HoughLineP function
# Higher Start Resolution decreases runtime
# Higher Angle Percision increases runtime
# Please refer to HoughLineP function for more information
def RotateByStraightLine(img, start_resolution=2, angle_percision=1440):
    temp_img=cv.resize(img,None, fx=0.5, fy=0.5, 
                       interpolation=cv.INTER_NEAREST)
    edges = cv.Canny(temp_img,100,150,apertureSize = 3)
    lines = cv.HoughLinesP(edges,start_resolution,np.pi/angle_percision,
                           100,minLineLength=750,maxLineGap=50)
    angles=[0.0]
    
    if(lines is None):
        print("Warning: Hough Line Algorithm can't detect lines")
    else:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            angle=np.arctan((y2-y1)/(x2-x1))/np.pi*180
            if(angle<5 and angle>-5):
                angles.append(angle)
            #cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    #cv.imwrite(temp_path+file_name+"_"+str(i)+".jpg",img)
    #End Generate Hough Line

    #Rotate
    rot_angle=np.median(angles)
    if(rot_angle!=0):
        (h, w) = img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        M = cv.getRotationMatrix2D((cX, cY), rot_angle, 1.0)
        img = cv.warpAffine(img, M, (w, h),
                                      flags=cv.INTER_CUBIC, borderValue=(127,127,127))
        #cv.imwrite(temp_path+file_name+"_"+str(i)+".jpg",img)
    return (img, rot_angle)
    #end if
    #End Rotate

# Shrink edges until 4 edges are white
# Use 2 Criterias
# Mean is the mean value of 1 edge (out of 4 in the image)
# Min is the minimum value of 1 edge
# These 2 values are to detect whether the current edge is white enough
# Step Size controls the update pace of the cropping edge
# Smaller step size is slower, and may capture some unwanted noise.
def CropWhite(img, H, W, Mean_Thresh=240, Min_Thresh=120, Step_Size=10):
    #Cropping
    #recorder of minimum brightness on edge (out of 255)
    edge_mean=0
    edge_min=0
    #Mean: Threshold of white (out of 255)
    #Min: Threshold of black (out of 255)
    #Step size of each cropping

    x0 = 0
    y0 = 0
    x1 = img.shape[:2][1]-1
    y1 = img.shape[:2][0]-1
    while((edge_mean<Mean_Thresh or edge_min<Min_Thresh)
           and x1-x0>W/3 and y1-y0>H/3):
        #Calculate Mean
        if(edge_mean<Mean_Thresh):
            mean_top=np.mean(img[y0,x0:x1])
            mean_left=np.mean(img[y0:y1,x0])
            mean_bottom=np.mean(img[y1,x0:x1])
            mean_right=np.mean(img[y0:y1,x1])
            edge_mean=min(mean_top,mean_left,mean_bottom,mean_right)
            if(edge_mean==mean_top):
                y0+=Step_Size
            elif(edge_mean==mean_left):
                x0+=Step_Size
            elif(edge_mean==mean_bottom):
                y1-=Step_Size
            elif(edge_mean==mean_right):
                x1-=Step_Size
        elif(edge_min<Min_Thresh):
            min_top=min(img[y0,x0:x1])
            min_left=min(img[y0:y1,x0])
            min_bottom=min(img[y1,x0:x1])
            min_right=min(img[y0:y1,x1])
            edge_min=min(min_top,min_left,min_bottom,min_right)
            if(edge_min==min_top):
                y0+=Step_Size
            elif(edge_min==min_left):
                x0+=Step_Size
            elif(edge_min==min_bottom):
                y1-=Step_Size
            elif(edge_min==min_right):
                x1-=Step_Size
    #end While
    return(img[y0:y1,x0:x1], x0, x1, y0, y1)


# Patch with size less than or equal to these threshold will be removed
# May dramatically improve quality on old printed books
# But not much on new books
def DespecklePatch(img, Despeckle_White_Size=5, Despeckle_Black_Size=10):
    
    White_Counter=0
    Black_Counter=0
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img, None, None, None, 4)
    areas  = stats[ : , cv.CC_STAT_AREA]
    left   = stats[ : , cv.CC_STAT_LEFT]
    top    = stats[ : , cv.CC_STAT_TOP]
    width  = stats[ : , cv.CC_STAT_WIDTH]
    height = stats[ : , cv.CC_STAT_HEIGHT]
    #small_label=np.where(areas<= Despeckle_White_Size)[0]+1
    
    for j in range(1 , nlabels):
        if areas[j] <= Despeckle_White_Size:
            White_Counter += 1
            for x in range(left[j], left[j] + width[j]):
                for y in range(top[j], top[j] + height[j]):
                    if labels[y, x] == j:
                        img[y, x] = 0
    
    #Now invert color and despeckle black
    img[:]=255-img
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img, None, None, None, 4)
    areas  = stats[ : , cv.CC_STAT_AREA]
    left   = stats[ : , cv.CC_STAT_LEFT]
    top    = stats[ : , cv.CC_STAT_TOP]
    width  = stats[ : , cv.CC_STAT_WIDTH]
    height = stats[ : , cv.CC_STAT_HEIGHT]
    
    for j in range(1 , nlabels):
        if areas[j] <= Despeckle_Black_Size:
            Black_Counter += 1
            for x in range(left[j], left[j] + width[j]):
                for y in range(top[j], top[j] + height[j]):
                    if labels[y, x] == j:
                        img[y, x] = 0

    #Invert color back to original
    return(255-img,White_Counter, Black_Counter)
    #End Despeckle


# Fit the image to the given canvas size.
# May pad or crop edges. 
# If cropping must be done, avoid cropping black parts 
# by calculating black areas on both sides
def FitToCanvas(img, Tgt_W, Tgt_H, Step_Size=10):
    #Fit to canvas
    #part of white edge being kept during centering, from 0.00 to 1.00
    Keep_White=0.2
    x0 = 0
    y0 = 0
    x1 = img.shape[:2][1]-1
    y1 = img.shape[:2][0]-1 
    while(x0<x1 and min(img[:,x0]==255)):
        x0+=Step_Size
    while(x1>x0 and min(img[:,x1]==255)):
        x1-=Step_Size
    while(y0<y1 and min(img[y0,:]==255)):
        y0+=Step_Size
    while(y1>y0 and min(img[y1,:]==255)):
        y1-=Step_Size
    #print(x0,x1,y0,y1)

    #Update cropping edges based on Keep_White
    x0=math.floor(x0*(1-Keep_White))
    y0=math.floor(y0*(1-Keep_White))
    x1=math.floor((img.shape[:2][1]-1)*Keep_White+x1*(1-Keep_White))
    y1=math.floor((img.shape[:2][0]-1)*Keep_White+y1*(1-Keep_White))
    img=img[y0:y1,x0:x1]
    #print(x1-x0,y1-y0)
    #Padding (or cropping)
    x0=int((Tgt_W-img.shape[:2][1])/2)
    x1=Tgt_W-img.shape[:2][1]-x0
    y0=int((Tgt_H-img.shape[:2][0])/2)
    y1=Tgt_H-img.shape[:2][0]-y0
    #print(x0,x1,y0,y1)
    if(x0+x1==-1):
        img=img[:,0:Tgt_W-x0]
    elif(x1<0 or x0<0):
        p0=255-np.mean(img[:,0:(0-x0)])
        p1=255-np.mean(img[:,(Tgt_W+x1):Tgt_W-1])
        if(p0==0 and p1!=0):
            x0+=x1
            x1=0
        elif(p1==0 and p0!=0):
            x1+=x0
            x0=0
        else:
            if(p0!=0 and p1!=0):
                #print(p0,p1)
                xsum=x0+x1
                x0=int(xsum*(p1/(p0+p1)))
                x1=xsum-x0
        img=img[:,(0-x0):(Tgt_W-x0)]
    else:
        img= cv.copyMakeBorder(img,0,0,x0,x1,cv.BORDER_CONSTANT,value=255)
    #End if(x)
    if(y0+y1==-1):
        img=img[0:Tgt_H,:]
    elif(y1<0 or y0<0):
        p0=255-np.mean(img[0:(0-y0),:])
        p1=255-np.mean(img[(Tgt_H+y1):Tgt_H-1,:])
        if(p0==0 and p1!=0):
            y0+=y1
            y1=0
        elif(p1==0 and p0!=0):
            y1+=y0
            y0=0
        else:
            if(p0!=0 and p1!=0):
                ysum=y0+y1
                y0=int(ysum*(p1/(p0+p1)))
                y1=ysum-y0
        img=img[(0-y0):(Tgt_H-y0),:]
    else:
        img= cv.copyMakeBorder(img,y0,y1,0,0,cv.BORDER_CONSTANT,value=255)
    return(img)
    #End if(y)

# Divide the 2 edges into N parts. 
# Check the thumbnail (in grayscale) of the resulting NxN matrix.
# Center the black part if possible.
# Center_Edge_Part is the N parts mentioned before
# Max LR Pixel is the max allowed distance of horizontal offset
# Max TB Pixel is ... of vertical offset
# You may not want to set these values too big
# Because some pages have contents that are not centered
def CenterImg(img, Center_Edge_Part=100, Max_LR_Pixels=280, Max_TB_Pixels=200):

    (Tgt_H, Tgt_W) = img.shape[:2]

    center_thumbnail=cv.resize(img,None, fx=0.5, fy=0.5)
    center_thumbnail=255-center_thumbnail
    center_thumbnail=cv.threshold(center_thumbnail, 200, 255, cv.THRESH_TOZERO)[1]
    center_thumbnail=255-center_thumbnail

    #cv.imwrite(final_path+file_name+"_TB_"+str(i)+".png",center_thumbnail)
    center_thumbnail=255-cv.resize(img,(Center_Edge_Part, Center_Edge_Part))
    top_blocks=0
    bottom_blocks=0
    left_blocks=0
    right_blocks=0
    sum_blocks=0
    while(sum_blocks==0 and top_blocks<Center_Edge_Part):
        sum_blocks=np.mean(center_thumbnail[top_blocks,:])
        top_blocks+=1
    sum_blocks=0
    while(sum_blocks==0 and bottom_blocks<Center_Edge_Part):
        sum_blocks=np.mean(center_thumbnail[Center_Edge_Part-bottom_blocks-1,:])
        bottom_blocks+=1
    sum_blocks=0
    while(sum_blocks==0 and left_blocks<Center_Edge_Part):
        sum_blocks=np.mean(center_thumbnail[:,left_blocks])
        left_blocks+=1
    sum_blocks=0 
    while(sum_blocks==0 and right_blocks<Center_Edge_Part):
        sum_blocks=np.mean(center_thumbnail[:,Center_Edge_Part-right_blocks-1])
        right_blocks+=1
    #print("TBLR:",top_blocks,bottom_blocks,left_blocks,right_blocks)
    #cv.imwrite(final_path+file_name+"_TB_"+str(i)+".png",center_thumbnail)

    LR_Offset=0
    AbsLR=abs(left_blocks-right_blocks)
    if(AbsLR>3):
        LR_Offset=min(AbsLR/2*Tgt_W/Center_Edge_Part,Max_LR_Pixels)
        LR_Offset*=0-AbsLR/(left_blocks-right_blocks)
        LR_Offset=int(LR_Offset)
    TB_Offset=0
    AbsTB=abs(top_blocks-bottom_blocks)
    if(AbsTB>3):
        TB_Offset=min(AbsTB/2*Tgt_H/Center_Edge_Part,Max_TB_Pixels)
        TB_Offset*=0-AbsTB/(top_blocks-bottom_blocks)
        TB_Offset=int(TB_Offset)

    M = np.float32([[1,0,LR_Offset],[0,1,TB_Offset]])
    return(cv.warpAffine(img,M,(Tgt_W,Tgt_H),borderValue=(255,255,255)), 
           LR_Offset, TB_Offset)
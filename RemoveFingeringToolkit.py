import cv2 as cv
import numpy as np

def EraseNonConnected(img, x, y, area_thresh=500, brushsize=12):
    H, W = img.shape[:2]
    x0=max(0, x-brushsize)
    y0=max(0, y-brushsize)
    x1=min(W-1, x+brushsize)
    y1=min(H-1, y+brushsize)
    if(np.average(img[y0:y1, x0:x1])<230):
        #print("decreasing brush size")
        brushsize=brushsize//2
        x0=max(0, x-brushsize)
        y0=max(0, y-brushsize)
        x1=min(W-1, x+brushsize)
        y1=min(H-1, y+brushsize)
    img[:]=255-img
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img, None, None, None, 4)
    areas  = stats[ : , cv.CC_STAT_AREA]
    left   = stats[ : , cv.CC_STAT_LEFT]
    top    = stats[ : , cv.CC_STAT_TOP]
    width  = stats[ : , cv.CC_STAT_WIDTH]
    height = stats[ : , cv.CC_STAT_HEIGHT]
    for x in range(x0, x1):
        for y in range(y0, y1):
            j=labels[y,x]
            if(areas[j]<area_thresh):
                for xt in range(left[j], left[j] + width[j]):
                    for yt in range(top[j], top[j] + height[j]):
                        if labels[yt, xt] == j:
                            img[yt, xt] = 0
    img[:]=255-img
    return(img)

def EraseConnected(img, x, y, brushsize=12):
    H, W = img.shape[:2]
    x0=max(0, x-brushsize)
    y0=max(0, y-brushsize)
    x1=min(W-1, x+brushsize) 
    y1=min(H-1, y+brushsize)
    col_count=x1-x0+1
    Thresh=80
    for y in range(y0, y1):
        row_sum=np.sum(img[y, x0:x1])
        row_avg=row_sum//col_count
        if(row_avg>Thresh):
            img[y, x0:x1]=255
    return(img)
        


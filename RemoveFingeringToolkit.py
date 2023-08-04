import cv2 as cv
import numpy as np


def EraseNonConnected(img, x, y, area_thresh=500, brushsize=12):
    H, W = img.shape[:2]
    x0 = max(0, x-brushsize)
    y0 = max(0, y-brushsize)
    x1 = min(W-1, x+brushsize)
    y1 = min(H-1, y+brushsize)
    if (np.average(img[y0:y1, x0:x1]) < 230):
        # print("decreasing brush size")
        brushsize = brushsize//2
        x0 = max(0, x-brushsize)
        y0 = max(0, y-brushsize)
        x1 = min(W-1, x+brushsize)
        y1 = min(H-1, y+brushsize)
    img[:] = 255-img
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(
        img, None, None, None, 4)
    areas = stats[:, cv.CC_STAT_AREA]
    left = stats[:, cv.CC_STAT_LEFT]
    top = stats[:, cv.CC_STAT_TOP]
    width = stats[:, cv.CC_STAT_WIDTH]
    height = stats[:, cv.CC_STAT_HEIGHT]
    for x in range(x0, x1):
        for y in range(y0, y1):
            j = labels[y, x]
            if (areas[j] < area_thresh):
                for xt in range(left[j], left[j] + width[j]):
                    for yt in range(top[j], top[j] + height[j]):
                        if labels[yt, xt] == j:
                            img[yt, xt] = 0
    img[:] = 255-img
    return (img)


def EraseConnected(img, x, y, brushsize=12):
    H, W = img.shape[:2]
    x0 = max(0, x-brushsize)
    y0 = max(0, y-brushsize)
    x1 = min(W-1, x+brushsize)
    y1 = min(H-1, y+brushsize)
    col_count = x1-x0+1
    Thresh = 80
    for y in range(y0, y1):
        row_sum = np.sum(img[y, x0:x1])
        row_avg = row_sum//col_count
        if (row_avg > Thresh):
            img[y, x0:x1] = 255
    return (img)


def GenerateEraseMask(img, area_thresh=500):
    img[:] = 255-img
    H, W = img.shape[:2]
    erase_mask = np.zeros((H, W), np.uint8)
    erase_mask[:] = 255-erase_mask
    nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(
        img, None, None, None, 4)
    areas = stats[:, cv.CC_STAT_AREA]
    left = stats[:, cv.CC_STAT_LEFT]
    top = stats[:, cv.CC_STAT_TOP]
    width = stats[:, cv.CC_STAT_WIDTH]
    height = stats[:, cv.CC_STAT_HEIGHT]
    for j in range(1, nlabels):
        # Enter complex checking only if shape is small enough, 
        # and if width< height (shape is vertical)
        if (areas[j] <= area_thresh) and width[j]<=height[j]:
            y_ax = left[j] + width[j]//2
            x_ax = top[j] + height[j]//2
            # Count number of color changes. >2 then complex
            # X axis
            color_change=0
            isComplex=False
            start_color=labels[x_ax, left[j]]
            if(start_color==j):
                color_change+=1
            for x in range(left[j], left[j] + width[j]-1):
                if(labels[x_ax, x] != labels[x_ax, x+1]):
                    color_change +=1
            if (labels[x_ax, left[j] + width[j]-1]!=j):
                color_change -=1
            if(color_change>2):
                isComplex=True

            # Y axis
            if(not isComplex):
                color_change=0
                start_color=labels[top[j], y_ax]
                if(start_color==j):
                    color_change+=1
                for y in range(top[j], top[j] + height[j]-1):
                    if(labels[y, y_ax] != labels[y+1, y_ax]):
                        color_change +=1
                if (labels[top[j] + height[j]-1, y_ax]!=j):
                    color_change -=1
                if(color_change>2):
                    isComplex=True

            # Change color if isComplex
            if(isComplex):
                for x in range(left[j], left[j] + width[j]):
                    for y in range(top[j], top[j] + height[j]):
                        if labels[y, x] == j:
                            erase_mask[y, x] = 0
    img[:] = 255-img
    return erase_mask

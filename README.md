# MusicScoreScanHelper
## Changelog
### v1.1 alpha
- Significantly improve the efficiency of rotation and despeckle. Now there's no need to worry about disabling despeckle for runtime.
- Special thanks to Flrrr https://github.com/Flrrr?tab=repositories for implementing most part of the new despeckle function.
- Also imported PIL just to change final DPI to 600. This cannot be done with OpenCV.
## Description
This is a Python Script that helps you (hopefully) process scanned documents. It is intended to process musical scores, which has straight lines indicating horizontal directions. It will also work fine for scanned text documents.<br />
This program has the following process:<br />
1. Rotating the image according to straight line<br />
2. Cropping edge outside the page<br />
(Resize the file and apply B&W filter according to the parameter between 2 and 3)
3. Despeckling small black and white patches<br />
4. Fitting into fixed page size<br />
5. Centering.<br />
Each part is put into a separate function in ```MusicScoreProc.py```. See detailed description in this file.<br />

## Important adjustment you need to make:<br />

### Start and end page:
- Some books have pictures or title as first few pages. The rotation function will waste time on these. 
- You can avoid it by changing the start page (```start_page```).
- If you only want to test this program on a few pages, set the end page (```page_num```) small.
### File Path:<br />
- This is obvious. In Windows, just follow the pattern given in the program.
- I don't have a Mac so you should figure it out yourself.
- Delete both Temp folders (```File_name_Temp``` and ```File_name```) before you run the same file name. You don't need to delete when using a different file name.
### Page Size:<br />
- The default ```4000x5400```, ```0.77``` Scaling is designed for 600 ppi scanning of A4 or similar page size.
- If you are scanning in other resolution or page size, you must change this.

## Other parameters in the main Python file:<br />
### ```Verbose```<br />
Print detailed rotation angle, crop amount, despeckled count and centering offset for each image.
Default value is ```True```.<br />
### ```Filter_Thresh```<br />
Determines at what value (0 to 255) the B&W Threshold cut off. Default value is ```160```.<br />
### ```Step_Size``` <br />
Controls the shrinking speed (in pixels) of crop edges. Small ```Step_Size``` will capture small dusts, and will be slow. But is less likely to miss data. Default value is ```10```.<br />
### ```UseStrongEnhance``` <br />
Not available until version ```alpha 1.3```. If enabled, generate an extra image that has higher threshold (keeping more black pixels), apply a strong despekle, and combines this image with the original image (Using ```cv.bitwise_and```). <br />
For some scans, parts of page is blurry, and this feature will partially restore those blurry parts. <br />
The side effect is that it will generate more black dots. If your scan is not blurry, it is not recommended to turn on. <br />
This will affect runtime and is by default ```False```. <br />

## Parameters in ```MusicScoreProc.py```:<br />
### ```RotateByStraightLine```
- ```start_resolution```: A parameter in ```cv.HoughLinesP```. Controls the start spacing of searching line. Larger value will increase processing speed.
- ```angle_percision```: A parameter in ```cv.HoughLinesP```. Controls the angle of rotation when searching lines. Larger value will decrease processing speed.
### ```CropWhite```
- ```H``` and ```W```: Designated output height and width. Can partially limit the maximum cropping amount, but is not working properly as of version ```alpha 1.2```.
- ```Mean_Thresh``` and ```Min_Thresh```: Stopping conditions. When both are satisfied, exit the cropping loop. ```Mean_Thresh``` calculates the minimum of average of each 4 sides. ```Min_Thresh``` finds the minimum on all 4 side.
- ```Step_Size```: The pace at which cropping line is moving.
### ```DespecklePatch```
- ```Despeckle_White_Size``` and ```Despeckle_Black_Size```: The maximum size of patches that will be erase. Patches being erased will invert their color. Setting these too large may mistakenly despeckle gap between notes and the staff, or small staccato dots. 
### ```FitToCanvas```
- The 3 adjustable parameters do the same thing as in ```CropWhite```. Please refer to that part.
### ```CenterImg```
- ```Center_Edge_Part```: Number of parts each edge will be divided into. Mean value will be calculated within each part to estimate the centering amount.
- ```Max_LR_Pixels``` and ```Max_TB_Pixels```: The length (in pixels) of maximum adjustment when centering. Will not affect anything if adjustment length is less than maximum. 

## Check out my test file <br />

https://www.mediafire.com/file/vw4re9p3pen2k55/Chopin_prelude_paderewski.pdf/file

- The Chopin Complete Edition by Paderewski is published in 1949. So it's copyright safe anywhere in the world (Except US). You can test this file and the runtime of this program (there is a built-in timer)<br />
- Please use the following parameters (Please note the following parameters are too fast for benchmark purpose, and will be changed in the next update):<br />
```sh
start_page=9
page_num=15
Verbose=True
UseDespeckle=True
```
- My computer with AMD 5900HX (Laptop) CPU and 32GB RAM finished this with 0 minutes and 11 second as of version 1.1 alpha.<br />
- The processed version of the above Chopin Prelude is now available on IMSLP<br />
https://imslp.org/wiki/Preludes,_Op.28_(Chopin,_Fr%C3%A9d%C3%A9ric)#IMSLP864159
  
  

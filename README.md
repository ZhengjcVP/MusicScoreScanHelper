# MusicScoreScanHelper
🌏 **[中文版](README_zh.md)**
## Changelog
### v1.5 alpha
The following changes are made regarding ```LoadScanPDFMain.py```and```MusicScoreProc.py```: <br />
- Added an input DPI function. For A4 or 8.5x11in scans that are not 600dpi, adjust this number.
- Added an alternative hough line detection for ```RotateByStraightLine```. If input resolution is too low, do not scale down. Decrease ```start_resolution``` and ```minLineLength```.
- Added an rotation option for odd/even page.
- Added a Pre-crop function for scanners with pre-exsisting white edge.
- Other changes that improve readability. (E.g. Merging ```StrongEnhance()``` into ```MusicScoreProc.py```, removing some comments etc.)

The following changes are made regarding ```RemoveFingeringToolkit.py```: <br />
- Added a ```GenerateEraseMask()``` function. Currently not used in the main program. It will mark all numbers except 1, which can help erase fingering. Merging into the main program will happen in a later update.
### v1.4 alpha
The following changes are made regarding ```RemoveFingeringMain.py```: <br />
- Previously, thumbnail is changed and these changes are reflected to the original image. This will cause the final image to be inaccurate. Now, no direct changes are made to the thumbnail. The original image is changed, and the thumbnail is updated.
- The thumbnail will automatically fit the size of screen (Under DPI Aware in Windows)
- Refresh rate is changed for window display . Previously, the image refreshes every 10 ms. Now, the image only refreshes when a change is made.
### v1.3 alpha
- Version 1.2 is ambiguous and therefore skipped.
- Added a strong enhance feature to partially restore blurry scans.
- Added a new program ```RemoveFingeringMain.py``` to allow users manually remove fingering.
- Also 2 abandoned files of testing new functionality. They are uploaded for backup purpose, and are not recommended to use. 
### v1.1 alpha
- Significantly improve the efficiency of rotation and despeckle. Now there's no need to worry about disabling despeckle for runtime.
- Special thanks to Flrrr https://github.com/Flrrr?tab=repositories for implementing most part of the new despeckle function.
- Also imported PIL just to change final DPI to 600. This cannot be done with OpenCV.

## File Structure
- ```LoadScanPDFMain.py```: The main file of rotating, cropping and filtering music score. See Description below.
- ```MusicScoreProc.py```: A collection of helper functions including rotation, cropping, despeckle, centering, etc.
- ```RemoveFingeringMain.py```: The main file of manual fingering removal.
- ```RemoveFingeringToolkit.py```: A collection of helper functions including removing patches and cleaning objects between lines.
- ```LoadScanPDFMainMP.py```: Abandoned file. Intended to boost main process by using multi-threading. The result is not efficient.
- ```CombinePDF.py```: Abandoned file. Intended to combine images into PDF. The resulting file is too large and not efficient.

## Description for ```LoadScanPDFMain.py```
This is a Python Script that helps you (hopefully) process scanned documents. It is intended to process musical scores, which has straight lines indicating horizontal directions. It will also work fine for scanned text documents.<br />
This program has the following process:<br />
1. Rotating the image according to straight line<br />
2. Cropping edge outside the page<br />
(Resize the file and apply B&W filter according to the parameter between 2 and 3)
3. Despeckling small black and white patches<br />
4. Fitting into fixed page size<br />
5. Centering.<br />
Each part is put into a separate function in ```MusicScoreProc.py```. See detailed description in this file.<br />

## Important adjustments you need to make (for ```LoadScanPDFMain.py```):<br />

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
- For A4 or similar scans but not in 600dpi, you can just change ```inDPI```. 
- For non-A4-or-similar scans, you must change the resolution.
- You can also linearly increase the resolution and scaling, which will generate images with higher resolution (But larger file size).

## Other parameters in ```LoadScanPDFMain.py```:<br />

### ```Verbose```<br />
Print detailed rotation angle, crop amount, despeckled count and centering offset for each image.
Default value is ```True```.<br />
### ```Filter_Thresh```<br />
Determines at what value (0 to 255) the B&W Threshold cut off. Default value is ```160```.<br />
### ```Step_Size``` <br />
Controls the shrinking speed (in pixels) of crop edges. Small ```Step_Size``` will capture small dusts, and will be slow. But is less likely to miss data. Default value is ```10```.<br />
### ```UseStrongEnhance``` <br />
If enabled, generate an extra image that has higher threshold (keeping more black pixels), apply a strong despekle, and combines this image with the original image (Using ```cv.bitwise_and```). <br />
For some scans, parts of page is blurry, and this feature will partially restore those blurry parts. <br />
The side effect is that it will generate more black dots. If your scan is not blurry, it is not recommended to turn on. <br />
This will affect runtime and is by default ```False```. <br />

## Parameters in ```MusicScoreProc.py```:<br />

### ```RotateByStraightLine```
- ```start_resolution```: A parameter in ```cv.HoughLinesP```. Controls the start spacing of searching line. Larger value will increase processing speed.
- ```angle_percision```: A parameter in ```cv.HoughLinesP```. Controls the angle of rotation when searching lines. Larger value will decrease processing speed.
### ```CropWhite```
- ```H``` and ```W```: Designated output height and width. Can partially limit the maximum cropping amount, but is still not working properly as of version ```alpha 1.4```.
- ```Mean_Thresh``` and ```Min_Thresh```: Stopping conditions. When both are satisfied, exit the cropping loop. ```Mean_Thresh``` calculates the minimum of average of each 4 sides. ```Min_Thresh``` finds the minimum on all 4 side.
- ```Step_Size```: The pace at which cropping line is moving.
### ```DespecklePatch```
- ```Despeckle_White_Size``` and ```Despeckle_Black_Size```: The maximum size of patches that will be erased. Patches being erased will invert their color. Setting these too large may mistakenly despeckle gap between notes and the staff, or small staccato dots. 
### ```FitToCanvas```
- The 3 adjustable parameters do the same thing as in ```CropWhite```. Please refer to that part.
### ```CenterImg```
- ```Center_Edge_Part```: Number of parts each edge will be divided into. Mean value will be calculated within each part to estimate the centering amount.
- ```Max_LR_Pixels``` and ```Max_TB_Pixels```: The length (in pixels) of maximum adjustment when centering. Will not affect anything if adjustment length is less than maximum. 

## Description for ```RemoveFingeringMain.py```
This file can help you manually erase fingerings. There are 4 input controls:
1. Left click and drag to erase non-connected components.
2. Middle click to erase components between lines within a square area. (Will keep the horizontal line and erase everything else)
3. Right click to Undo (Up to 2 steps).
4. Escape (Esc) to end current image and enter next image.

## Important adjustments you need to make (for ```RemoveFingeringMain.py```):<br />

### File Path, File Name, and Page Number:<br />
- These must be adjusted correctly so that the program can read the file. The program cannot automatically read all PNG images in a folder, so page number must be continuous, and must start and end with existing file.

### Window_Size:<br />
- As of ```v1.4 alpha```, ```Scaling``` is automatically adjusted according to screen resolution. There is no use in changing it.
- ```Window_size``` will control the size displayed on screen. ```0.9``` will almost take up the full screen, while ```0.5``` takes 1/4 of the screen (half for both H and W). Value greater than ```1.0``` will not properly display image.
- I don't know how to check DPI and screen resolution for other OS, so you must change related parts if you are not using Windows.

## Check out my test file <br />

https://www.mediafire.com/file/vw4re9p3pen2k55/Chopin_prelude_paderewski.pdf/file

- The Chopin Complete Edition by Paderewski was published in 1949. So it's copyright safe anywhere in the world (Except US). You can test this file and the runtime of this program (there is a built-in timer)
- Please use the following parameters (adjusted in the new ```1.3 alpha``` update):<br />
```sh
start_page=9
page_num=100
Verbose=True
UseDespeckle=True
```
- My computer with AMD 5900HX (Laptop) CPU and 32GB RAM finished this with 2 minutes and 16 second as of version ```1.3 alpha```.
- The processed version of the above Chopin Prelude is now available on IMSLP
https://imslp.org/wiki/Preludes,_Op.28_(Chopin,_Fr%C3%A9d%C3%A9ric)#IMSLP864159
- The Ekier 1990 Chopin Etude and Henle Chopin Etude Op.10 (with fingering removed) are also available on IMSLP (Processed with the scripts here). The original scans of these file may not be made public. You can try the file above to test fingering removing function.
  
Also, for testing ```StrongEnhance()``` function, use the file below: <br/>
https://www.mediafire.com/file/yp59mbd0y7ca5qy/Chopin_ballades_henle_1976_p10-19.pdf/file
- This is a partially blurry scan that ```StrongEnhance()``` works well on. 
- Since fingerings are also contained in this scan, only 10 pages are provided, which is sufficient for testing purposes.

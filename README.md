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
3. Despeckling small black and white patches<br />
4. Fitting into fixed page size<br />
5. Centering.<br />
Each part is put into a separate function in ```MusicScoreProc.py```. See detailed description in this file.<br />

## Important adjustment you need to make:<br />

### Start and end page:
- Some books have pictures or title as first few pages. The rotation function will waste time on these. <br />
- You can avoid it by changing the start page.<br />
- If you only want to test this program on a few pages, set the end page (page_num) small.<br />
### File Path:<br />
- This is obvious. In Windows, just follow the pattern given in the program.<br />
- I don't have a Mac so you should figure it out yourself.<br />
- Delete both Temp folders (```File_name_Temp``` and ```File_name```) before you run the same file name. You don't need to delete when using a different file name
### Page Size:<br />
- The default ```4000x5400```, ```0.77``` Scaling is designed for 600 ppi scanning of A4 or similar page size.<br />
- f you are scanning in other resolution or page size, you must change this.<br />
### Despeckle:<br />
- As of version 1.1 alpha. Despeckle is very efficient and there is no need to turn off.

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
  
  

# MusicScoreScanHelper
<br />
Changelog<br />
v1.1 alpha<br />
Significantly improve the efficiency of rotation and despeckle.<br />
Now there's no need to worry about disabling despeckle for runtime.<br />
Special thanks to Flrrr https://github.com/Flrrr?tab=repositories <br />
for implementing most part of the new despeckle function.<br />
<br />
Also imported PIL just to change final DPI to 600. This cannot be done with OpenCV<br />

This is a Python Script that helps you (hopefully) process scanned documents. <br />
It is intended to process musical scores, which has straight lines indicating horizontal directions.<br />
It will also work fine for scanned text documents.<br />
This program has the following process:
1. Rotating the image according to straight line
2. Cropping edge outside the page
3. Despeckling small black and white patches
4. Fitting into fixed page size
5. Centering
Each part is put into a separate function in MusicScoreProc.py<br />

Important adjustment you need to make:<br />
Start and end page:<br />
Some books have pictures or title as first few pages. The rotation function will waste time on these. <br />
You can avoid it by changing the start page.<br />
If you only want to test this program on a few pages, set the end page (page_num) small.<br />
File Path:<br />
  This is obvious. In Windows, just follow the pattern given in the program.<br />
  I don't have a Mac so you should figure it out yourself.<br />
Page Size:<br />
  The default 4000x5400, 0.77 Scaling is designed for 600 ppi scanning of A4 or similar page size.<br />
  If you are scanning in other resolution or page size, you must change this.<br />
Despeckle:<br />
  As of version 1.1 alpha. Despeckle is very efficient and there is no need to turn off.
<br />
Check out my test file.<br />
  https://www.mediafire.com/file/vw4re9p3pen2k55/Chopin_prelude_paderewski.pdf/file<br />
  The Chopin Complete Edition by Paderewski is published in 1949. So it's copyright safe anywhere in the world (Except US)<br />
  You can test this file and the runtime of this program (there is a built-in timer)<br />
  Please use:<br />
    start_page=9<br />
    page_num=15<br />
    Verbose=True<br />
    UseDespeckle=True<br />
  My computer with AMD 5900HX (Laptop) CPU and 32GB RAM finished this with 0 minutes and 11 second.<br />
  

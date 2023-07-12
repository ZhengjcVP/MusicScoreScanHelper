# MusicScoreScanHelper
<br />
Changelog<br />
v1.1 alpha<br />
&emsp;Significantly improve the efficiency of rotation and despeckle.<br />
&emsp;Now there's no need to worry about disabling despeckle for runtime.<br />
&emsp;Special thanks to Flrrr https://github.com/Flrrr?tab=repositories <br />
&emsp;for implementing most part of the new despeckle function.<br />
<br />
&emsp;Also imported PIL just to change final DPI to 600. This cannot be done with OpenCV<br />
<br />
This is a Python Script that helps you (hopefully) process scanned documents. <br />
It is intended to process musical scores, which has straight lines indicating horizontal directions.<br />
It will also work fine for scanned text documents.<br />
This program has the following process:<br />
&emsp;1. Rotating the image according to straight line<br />
&emsp;2. Cropping edge outside the page<br />
&emsp;3. Despeckling small black and white patches<br />
&emsp;4. Fitting into fixed page size<br />
&emsp;5. Centering<br />
Each part is put into a separate function in MusicScoreProc.py<br />

Important adjustment you need to make:<br />
&emsp;Start and end page:<br />
&emsp;&emsp;Some books have pictures or title as first few pages. The rotation function will waste time on these. <br />
&emsp;&emsp;You can avoid it by changing the start page.<br />
&emsp;&emsp;If you only want to test this program on a few pages, set the end page (page_num) small.<br />
&emsp;File Path:<br />
&emsp;&emsp;This is obvious. In Windows, just follow the pattern given in the program.<br />
&emsp;&emsp;I don't have a Mac so you should figure it out yourself.<br />
&emsp;Page Size:<br />
&emsp;&emsp;The default 4000x5400, 0.77 Scaling is designed for 600 ppi scanning of A4 or similar page size.<br />
&emsp;&emsp;If you are scanning in other resolution or page size, you must change this.<br />
&emsp;Despeckle:<br />
&emsp;&emsp;As of version 1.1 alpha. Despeckle is very efficient and there is no need to turn off.
<br />
<br />
Check out my test file.<br />
&emsp; https://www.mediafire.com/file/vw4re9p3pen2k55/Chopin_prelude_paderewski.pdf/file<br />
&emsp;The Chopin Complete Edition by Paderewski is published in 1949. So it's copyright safe anywhere in the world (Except US)<br />
&emsp;You can test this file and the runtime of this program (there is a built-in timer)<br />
&emsp;Please use:<br />
&emsp;&emsp;start_page=9<br />
&emsp;&emsp;page_num=15<br />
&emsp;&emsp;Verbose=True<br />
&emsp;&emsp;UseDespeckle=True<br />
&emsp;My computer with AMD 5900HX (Laptop) CPU and 32GB RAM finished this with 0 minutes and 11 second.<br />
&emsp;The processed version of the above Chopin Prelude is now available on IMSLP<br />
&emsp;https://imslp.org/wiki/Preludes,_Op.28_(Chopin,_Fr%C3%A9d%C3%A9ric)#IMSLP864159
  
  

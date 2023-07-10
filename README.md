# MusicScoreScanHelper
This is a Python Script that helps you (hopefully) process scanned documents. 
It is intended to process musical scores, which has straight lines indicating horizontal directions.
It will also work fine for scanned text documents.
This program has the following process:
1. Rotating the image according to straight line
2. Cropping edge outside the page
3. Despeckling small black and white patches (Very time consuming. Can be turned off)
4. Fitting into fixed page size
5. Centering
Each part is put into a separate function in MusicScoreProc.py

Important adjustment you need to make:
Start and end page:
  Some books have pictures or title as first few pages. The rotation function will waste time on these. 
  You can avoid it by changing the start page.
  If you only want to test this program on a few pages, set the end page (page_num) small.
File Path:
  This is obvious. In Windows, just follow the pattern given in the program.
  I don't have a Mac so you should figure it out yourself.
Page Size:
  The default 4000x5400, 0.77 Scaling is designed for 600 ppi scanning of A4 or similar page size.
  If you are scanning in other resolution or page size, you must change this.
Despeckle:
  As said before. This is very time consuming. But it will improve quality (and reduce file size for a little bit)
  on old scanned files. For newer books, it has little effect.
  Turn it off if you think it's too slow.

Check out my test file.
  https://www.mediafire.com/file/vw4re9p3pen2k55/Chopin_prelude_paderewski.pdf/file
  The Chopin Complete Edition by Paderewski is published in 1949. So it's copyright safe anywhere in the world (Except US)
  You can test this file and the runtime of this program (there is a built-in timer)
  Please use:
    start_page=9
    page_num=15
    Verbose=True
    UseDespeckle=True
  My computer with AMD 5900HX (Laptop) CPU and 32GB RAM finished this with 4 minutes and 1 second.

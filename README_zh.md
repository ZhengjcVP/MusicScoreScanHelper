# MusicScoreScanHelper
🌏 **[English](README.md)**
## 更新日志
### v1.5 alpha
以下为 ```LoadScanPDFMain.py```和```MusicScoreProc.py```的变化: <br />
- 增加输入DPI功能. 对于 A4 或 8.5x11in 的，非 600dpi的纸张, 请调整此数值.
- 在 ```RotateByStraightLine```增加额外霍夫线变换功能. 如果输入分辨率过低，不执行降分辨率操作，并减小 ```start_resolution``` 和 ```minLineLength```.
- 可选奇数/偶数页进行旋转
- 增加预先裁剪功能，针对自动留白边的扫描仪。
- 其他增加可读性的调整（诸如将```StrongEnhance()```并入```MusicScoreProc.py```，删除无效注释等）

以下改进针对 ```RemoveFingeringToolkit.py```函数: <br />
- 增加一个 ```GenerateEraseMask()``` 函数。 目前在主程序没有使用。可以检测除了1以外的数字，有效帮助检测指法。将在之后的更新并入主程序。 
### v1.4 alpha
以下为 ```RemoveFingeringMain.py```的变化: <br />
- 之前的运算模式为修改缩略图，再基于缩略图的修改调整原始图。这样最终图片会不准确。新算法下，缩略图不被直接更改。直接修改原图，原图的变化反映在缩略图上。
- 缩略图会自动适应屏幕大小 (开启Windows系统的 DPI Aware 模式)
- 刷新率调整。之前每隔10ms刷新一次缩略图，现在只有当做出改变的时候再刷新缩略图。
### v1.3 alpha
- 1.2 版本因操作失误，意义不明，因此跳过。
- 针对模糊的扫描件，增加了一个可开关的硬增强（Strong Enhance）功能。
- 增加全新文件 ```RemoveFingeringMain.py``` 可以让用户手动删除指法.
- 增加了2个废弃文件。上传仅作为备份目的。
### v1.1 alpha
- 显著提高旋转和除尘功能的速度。现在无需担心运行时间。
- 特别感谢用户 Flrrr https://github.com/Flrrr?tab=repositories 完成了新除尘算法的大部分编写.
- 导入了 PIL 组建只因调整最终DPI为600。OpenCV没有此功能。

## 文件结构
- ```LoadScanPDFMain.py```: 主程序，负责旋转，裁切和加滤镜。详见下方说明。
- ```MusicScoreProc.py```: 辅助函数合集，包括旋转，裁切，除尘，居中等。
- ```RemoveFingeringMain.py```: 删除指法主程序。
- ```RemoveFingeringToolkit.py```: 辅助删除指法的函数合集，包括删除独立部分和删除线内数字。
- ```LoadScanPDFMainMP.py```: 被遗弃的文件。原本打算多线程处理载入PDF流程，但实际效率几乎没有提升。
- ```CombinePDF.py```: 被遗弃的文件。原本打算合并PDF，但是最终文件大小过大，效率极低。

## 文件 ```LoadScanPDFMain.py``` 说明
这个Python脚本（希望）能帮助你处理扫描文件。它的设计初衷是处理乐谱，因为有直线表示水平方向。对于纯文本扫描件也有不错的效果。<br />
本程序有以下步骤：<br />
1. 基于水平直线旋转程序<br />
2. 裁切页面外的部分<br />
（在步骤2和3之间，进行黑白滤镜和缩放）
3. 删除极小的黑白色块<br />
4. 将图片放入固定大小纸张内<br />
5. 居中<br />
每一个部分都在 ```MusicScoreProc.py```程序里有对应函数. 请见该程序介绍.<br />

## 必须做的调整 (对文件 ```LoadScanPDFMain.py```):<br />

### 开始和结束页:
- 有些书的开始页是图片或者标题，旋转函数会在此浪费很多时间。 
- 为了避免这种情况，可以调整开始页 （```start_page```）。
- 如果你只是想测试滤镜效果，可以把结束页 （```page_num```） 调小。
### 文件路径:<br />
- 显然这需要调整。在Windows系统下，请根据文件内已有格式调整。
- 我并没有Mac电脑，所以您需要自己研究。
- 在运行同一个文件名（```file_name```）之前，务必删除所有临时文件夹（```File_name_Temp``` 和 ```File_name```） . 对于不同文件名不需要此操作。
### 纸张大小:<br />
- 默认输出分辨率为 ```4000x5400```, 缩放```0.77``` 这些参数是为 600 ppi 扫描件，A4或类似大小纸张设计的。
- 如果你扫描的是A4或类似纸张，但不是600dpi，你可以直接调整输入DPI（```inDPI```）
- 如果你扫描的不是A4或类似纸张，务必调整输出分辨率
- 也可以线性缩放分辨率和缩放比例，这样可以增加最终图像清晰度，但文件大小也会提升。

## 在 ```LoadScanPDFMain.py```文件中的其他参数:<br />

### ```Verbose```<br />
输出具体的旋转角度，裁切坐标，除尘数量，居中位移等调整值。默认为 ```True```.<br />
### ```Filter_Thresh```<br />
决定黑白滤镜（0到255）的阈值，默认为 ```160```.<br />
### ```Step_Size``` <br />
控制裁边时的步长。小的 ```Step_Size``` 会捕捉小噪点，速度也更慢。但同时也不容易错过信息。默认值是 ```10```.<br />
### ```UseStrongEnhance``` <br />
若开启，再生成一个黑白滤镜阈值更高的图片（这样这个图片的黑像素点更多）使用更强的除尘参数，再和原图合并 (使用 ```cv.bitwise_and```). <br />
对于部分扫描件，页面的一部分会模糊，这个算法可以部分补回模糊的部分 <br />
副作用是图像会有更多黑点。如果扫描件不模糊，应该关掉。 <br />
会影响运行时间，默认为 ```False```. <br />

## 文件 ```MusicScoreProc.py```的函数:<br />

### ```RotateByStraightLine```
- ```start_resolution```: 函数 ```cv.HoughLinesP```的参数之一。 控制搜索线开始的间距。数值越大，程序运行速度越快。
- ```angle_percision```: 函数 ```cv.HoughLinesP```的参数之一。 控制搜索线旋转角度的间距，数值越大，程序越慢。
### ```CropWhite```
- ```H``` 和 ```W```: 指定的输出高度和宽度。 可以限制最大裁切幅度，但是在 ```alpha 1.4```版本并未起应有作用.
- ```Mean_Thresh``` 和 ```Min_Thresh```: 停止条件。当两者都满足时，退出循环 ```Mean_Thresh``` 计算四边每边平均的最小值。 ```Min_Thresh``` 计算四边的最小值。
- ```Step_Size```: 裁切线的推进速度。
### ```DespecklePatch```
- ```Despeckle_White_Size``` 和 ```Despeckle_Black_Size```: 最大除尘块的大小。过大会导致移除音符和行之间的间隙或者断奏点等记号。 
### ```FitToCanvas```
- 可调参数和 ```CropWhite```一致请参见该部分。
### ```CenterImg```
- ```Center_Edge_Part```: 每边被分割成的部分。每个部分会计算平均值，决定居中偏移量
- ```Max_LR_Pixels``` 和 ```Max_TB_Pixels```: 决定了居中的最大左右偏移量和上下偏移量。如果计算出的偏移量小于改值，则不影响。

## 文件 ```RemoveFingeringMain.py```描述
本文件可以协助删除指法。主要有以下4个操作：
1. 左击拖拽删除独立的部分。
2. 鼠标中键，删除一个方块内，水平线之间的部分（保留水平线，删掉其他部分）
3. 右击撤回至上一步（最多2步）
4. 退回 (Esc) 结束当前图片，进入下一图片。

## 必须的调整 (对文件 ```RemoveFingeringMain.py```):<br />

### 文件路径，文件名，和页码数<br />
- 必须调整这些参数，程序才能正确读入文件。本程序不能自动读取某文件夹的所有PNG文件，所以须确保页码连续，初始和结束页码均有文件存在。

### 窗口大小：<br />
- 在 ```v1.4 alpha```版本中， ```Scaling``` （缩放）是自动根据桌面大小调整的。调节这个变量大没有任何作用。
- ```Window_size``` 控制窗口的缩放比例。```0.9``` 就会基本占满全屏，而 ```0.5``` 会占据 1/4 个屏幕 （长宽各占一半）. 大于 ```1.0``` 的数值会导致无法正常显示图像。
- 我不清楚对于其他操作系统如何查询分辨率和屏幕DPI，因为若您不使用Windows，必须更改相关部分。

## 看一下我的测试文件 <br />

https://www.mediafire.com/file/vw4re9p3pen2k55/Chopin_prelude_paderewski.pdf/file

- 肖邦全集帕德雷夫斯基版是1949年出版的，因此在全世界均无版权问题（美国除外）你可以用此文件测试程序运行时间（有自带计时器）
- 请使用以下参数 （```1.3 alpha``` 版本更新）:<br />
```sh
start_page=9
page_num=100
Verbose=True
UseDespeckle=True
```
- 我的电脑使用 AMD 5900HX（笔记本）CPU 和 32GB RAM， 在```1.3 alpha```版本的运行时间是2分钟16秒.
- 处理完的该版本肖邦前奏曲已上传IMSLP
https://imslp.org/wiki/Preludes,_Op.28_(Chopin,_Fr%C3%A9d%C3%A9ric)#IMSLP864159
- 使用本程序处理并删除指法的1990版Ekier肖邦练习曲和亨乐版肖邦练习曲Op.10也已上传IMSLP。但原始文件不便公开，请使用上方文件测试删指法功能。
  
同时，为了测试 ```StrongEnhance()```函数，可以使用以下文件： <br/>
https://www.mediafire.com/file/yp59mbd0y7ca5qy/Chopin_ballades_henle_1976_p10-19.pdf/file
- 这是一个局部较模糊的扫描件，函数 ```StrongEnhance()```对此效果较好 
- 考虑到本文件含有指法，只提供10页，足够进行测试目的。

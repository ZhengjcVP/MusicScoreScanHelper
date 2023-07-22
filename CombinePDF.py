from PIL import Image
import os
def CombineImg2PDF(inpath, outpath):
    files=os.listdir(inpath)
    png_files = []
    sources = []
    for file in files:
        if 'png' in file or 'jpg' in file:
            png_files.append(inpath+file)
            png_files.sort()
    output = Image.open(png_files[0])
    png_files.pop(0)
    for file in png_files:
        print("updated")
        png_file = Image.open(file)
        #if png_file.mode == "RGB":
        #    png_file = png_file.convert("RGB")
        sources.append(png_file)
    output.save(outpath, "pdf", save_all=True, append_images=sources)

CombineImg2PDF("D:\\Documents\\Homework\\Python\\PDFProj\\Chopin Ballade\\",
                "D:\\Documents\\Homework\\Python\\PDFProj\\Chopin Ballade\\out.pdf")


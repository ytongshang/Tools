# encoding=utf-8

# brew install webp
# brew install phthon3
# pip3 install Pillow
# python3 webp.py -i [要转换的图片目录]  -q [图片质量，不传默认为80]

import os
import sys
import getopt
import shutil
import subprocess
from PIL import Image

input_file = ""
quality = "80"
outputPath = input_file + "_webp"


def handle_sys_arguments():
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:q:")
    global quality
    global output_file
    global input_file

    for op, value in opts:
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_file = value
        elif op == "-q":
            quality = value
        elif op == "-h":
            print("-i 要压缩的图片文件夹目录\n -q 压缩图片质量  默认80")
            exit()


def walk_through(path):
    for i in os.listdir(path):
        new_path = os.path.join(path, i)
        if os.path.isfile(new_path):
            to_webp(new_path)
        else:
            walk_through(new_path)


def to_webp(filePath):
    split_name = os.path.splitext(filePath)

    if split_name[1] == ".webp":
        # webp 不用转化
        return
    if split_name[1] != ".jpg" and split_name[1] != ".png":
        return
    print("")
    print("###############################################")
    transformFile = filePath
    if split_name[1] == ".png":
        # 如果是png,先转成jpg,去掉alpha通道
        # 然后jpg 转webp
        jpgFile = split_name[0] + ".jpg"
        if (png2jpg(filePath, jpgFile)):
            transformFile = jpgFile
    command = "cwebp -q " + quality + " " + \
        transformFile + " -o " + split_name[0] + ".webp"
    subprocess.call(command, shell=True)


def IsValidImage(img_path):
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False
    return bValid


def png2jpg(pngFile, jpgFile):
    if IsValidImage(pngFile):
        try:
            im = Image.open(pngFile)
            im.save(jpgFile)
            print("png2jpg success:" + pngFile)
            return True
        except:
            print("png2jpg failure:" + pngFile)
            os.remove(jpgFile)
            return False
    else:
        print("png2jpg failure:" + pngFile)
        return False


def check_args():
    if input_file.strip() == "":
        print("请输入要转换的文件夹路径")
        exit()


def copy_webp_files(sourceDir, targetDir):
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    for file in os.listdir(sourceDir):
        new_source_path = os.path.join(sourceDir, file)
        if os.path.isdir(new_source_path):
            new_target_path = os.path.join(targetDir, file)
            copy_webp_files(new_source_path, new_target_path)
        else:
            splite_name = os.path.splitext(file)
            if splite_name[1] == ".webp":
                continue
            print("###############################################")
            copyName = file
            copyPath = new_source_path
            originSize = os.path.getsize(new_source_path)
            print(new_source_path + " originSize:" + str(originSize))
            webpName = splite_name[0] + ".webp"
            webpPath = os.path.join(sourceDir, webpName)
            isWebpExist = False
            if os.path.exists(webpPath):
                webpSize = os.path.getsize(webpPath)
                isWebpExist = True
                print(webpPath + " webpSize:" + str(webpSize))
                if webpSize < originSize:
                    copyName = webpName
                    copyPath = webpPath
                    print("webp格式小于原图大小，选择webp")
                else:
                    copyName = file
                    copyPath = new_source_path
                    print("原图小于webp，选择原图")
            new_target_path = os.path.join(targetDir, copyName)
            shutil.copy(copyPath, new_target_path)
            if isWebpExist:
                os.remove(webpPath)


if __name__ == '__main__':
    handle_sys_arguments()
    check_args()
    walk_through(input_file)
    copy_webp_files(input_file, outputPath)

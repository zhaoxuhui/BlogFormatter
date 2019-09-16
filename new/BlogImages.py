# coding=utf-8
import cv2
import os
import datetime
import tinify
import sys
from PIL import Image
import shutil


# 脚本功能
# 1.批量读取、改名
# 2.批量修改大小
# 3.批量压缩
# 4.自动插入标签

def findAllFiles(root_dir, filter):
    """
    在指定目录查找指定类型文件

    :param root_dir: 查找目录
    :param filter: 文件类型
    :return: 路径、名称、文件全路径

    """

    separator = os.path.sep
    paths = []
    names = []
    files = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(filter):
                paths.append(parent + separator)
                names.append(filename)
    for i in range(paths.__len__()):
        files.append(paths[i] + names[i])
    paths.sort()
    names.sort()
    files.sort()
    return paths, names, files

# 读取目录下所有图片的路径，返回一个list
def findAllImages(root_dir):
    paths = []
    # 遍历
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".PNG") or filename.endswith(".JPG") or filename.endswith(".gif") or filename.endswith(".GIF") or filename.endswith(".mp4") or filename.endswith(".MP4") or filename.endswith(".avi") or filename.endswith(".AVI"):
                paths.append(parent + "\\" + filename)
    print "All images loaded."
    return paths


# 获取当前系统的日期
def getDateString():
    return datetime.datetime.now().strftime('%Y-%m-%d')


# 基于读取的图片路径和当前日期，拼接组成新的符合格式的文件名
def generateFormatName(paths, start_index):
    new_names = []
    root = paths[0][0: paths[0].rfind("\\")] + "\\"
    for i in range(len(paths)):
        new_name = root + getDateString() + "-" + '{:0>2}'.format(i + 1 + start_index) + "." + paths[i].split(".")[-1]
        new_names.append(new_name)
    return new_names


# 批量将文件重命名
def renameImages(ori, new):
    for i in range(len(new)):
        os.rename(ori[i], new[i])
    print "All images are renamed."


# 修改图片大小
def resizeImage(img):
    width = img.shape[1]
    new_width = 0
    if width > 650:
        new_width = 650
    elif 650 > width >= 625:
        new_width = 625
    elif 625 > width >= 600:
        new_width = 600
    elif 600 > width >= 575:
        new_width = 575
    elif 575 > width >= 550:
        new_width = 550
    elif 550 > width >= 525:
        new_width = 525
    elif 525 > width >= 500:
        new_width = 500
    elif 500 > width >= 475:
        new_width = 475
    elif 475 > width >= 450:
        new_width = 450
    elif 450 > width >= 425:
        new_width = 425
    elif 425 > width >= 400:
        new_width = 400
    elif 400 > width >= 375:
        new_width = 375
    elif 375 > width >= 350:
        new_width = 350
    elif 350 > width > 325:
        new_width = 325
    elif 325 > width > 300:
        new_width = 300
    elif 300 > width >= 275:
        new_width = 275
    elif 275 > width >= 250:
        new_width = 250
    elif 250 > width >= 225:
        new_width = 225
    elif 225 > width >= 200:
        new_width = 200
    elif 200 > width >= 175:
        new_width = 175
    elif 175 > width >= 150:
        new_width = 150
    elif 150 > width >= 125:
        new_width = 125
    elif 125 > width >= 100:
        new_width = 100
    elif 100 > width >= 75:
        new_width = 75
    elif 75 > width >= 50:
        new_width = 50
    elif 50 > width >= 0:
        new_width = 50

    ratio = new_width * 1.0 / width
    if ratio == 0:
        ratio = 1

    res = cv2.resize(img, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_CUBIC)
    return res


# 批量修改图片大小并输出覆盖原图
def saveImages(new):
    for item in new:
        if item.endswith(".jpg") or item.endswith(".png") or item.endswith(".PNG") or item.endswith(".JPG"):
            img = cv2.imread(item)
            img2 = resizeImage(img)
            cv2.imwrite(item, img2)
    print "All images are resized."


# 调用TinyPNG接口进行图像压缩，并替换原图
def tinifyImage(image_paths):
    for i in range(len(image_paths)):
        if image_paths[i].endswith(".jpg") or image_paths[i].endswith(".png") or image_paths[i].endswith(".PNG") or image_paths[i].endswith(".JPG"):
            source = tinify.from_file(image_paths[i])
            source.to_file(image_paths[i])
            print "Compress", format((i * 1.0 / len(image_paths)) * 100, '0.2f'), "% finished.", image_paths[i]
    print "Compress 100% finished."


# 根据文件路径生成img标签
def generateHTML(html1, html2, html3, new_paths, root):
    f = open(root + "\\img_tag.txt", "w")
    for item in new_paths:
        if cv2.imread(item).shape[1]>680:
            f.write(html1 + item[item.rfind("\\") + 1:] + html2 + '680' + html3 + "\n")
        else:
            f.write(html1 + item[item.rfind("\\") + 1:] + html2 + cv2.imread(item).shape[1].__str__() + html3 + "\n")
    f.close()
    print "HTML tag generated successfully."


# 根据"<-img"标签自动插入图片Tag
def insertImgTag(html1, html2, html3, new_paths, file_path):
    img_tags = []
    i = 0
    out = ""

    for item in new_paths:
        if item.endswith(".jpg") or item.endswith(".png") or item.endswith(".PNG") or item.endswith(".JPG"):
            if cv2.imread(item).shape[1]>680:
                img_tag = html1 + item[item.rfind("\\") + 1:] + html2 + '680' + html3 + "\n"
            else:
                img_tag = html1 + item[item.rfind("\\") + 1:] + html2 + cv2.imread(item).shape[1].__str__() + html3 + "\n"
            img_tags.append(img_tag)
        elif item.endswith(".gif") or item.endswith(".GIF"):
            im = Image.open(item, "r")
            width = im.size[0]
            height = im.size[1]
            if width>660:
                gif_tag = html1 + item[item.rfind("\\") + 1:] + html2 + '660' + html3 + "\n"
            else:
                gif_tag = html1 + item[item.rfind("\\") + 1:] + html2 + width.__str__() + html3 + "\n"
            img_tags.append(gif_tag)
        elif item.endswith(".mp4") or item.endswith(".MP4") or item.endswith(".avi") or item.endswith(".AVI"):
            cap = cv2.VideoCapture(item)
            width = int(cap.get(3))
            height = int(cap.get(4))
            url = "https://zhaoxuhui.top/assets/images/blog/content/"+item.split("\\")[-1]
            if width<660:
                video_tag = "<p align=\"center\"><video width=\""+width.__str__()+"\" height=\""+height.__str__()+"\" controls><source src=\""+url+"\" type=\"video/mp4\">您的浏览器不支持 HTML5 video 标签。</video></p>\n"
            else:
                video_tag = "<p align=\"center\"><video width=\""+int((660.0/width)*width).__str__()+"\" height=\""+int((660.0/width)*height).__str__()+"\" controls><source src=\""+url+"\" type=\"video/mp4\">Your broswer doesn't support HTML5 video tag.</video></p>\n"
            img_tags.append(video_tag)

    f = open(file_path)
    lines = f.readlines()
    for line in lines:
        if line.__contains__("<-img") or line.__contains__("<-gif") or line.__contains__("<-video"):
            line = img_tags[i]
            i += 1
        out += line
    f.close()
    f = open(file_path.split('.')[-2] + "_auto.md", "w")
    f.writelines(out)
    f.close()
    print("save success")


def execImgs():
    # 你的TinyPNG密钥
    tinify.key = "X-MOCVLhlFTeKJCIhHD-etqYwYmflH4p"

    # HTML img标签
    html_part1 = "<img src = \"https://zhaoxuhui.top/assets/images/blog/content/"
    html_part2 = "\" width = \""
    html_part3 = "\">"

    our_res = ""

    # 用户指定图片所在目录
    flag0 = raw_input("\nAuto input img path?[y]/n\n")
    if flag0 == "" or flag0 == "y" or flag0 == "Y":
        root_dir  = os.getcwd()+os.sep+"imgs"+os.sep
    else:
        root_dir = raw_input("Input the parent path of images:\n")

    # 第一步，获取目录下所有图片路径
    ori = findAllImages(root_dir)

    # 如果没有图片，直接复制
    if len(ori) == 0:
        print("No images.")
        flag4 = raw_input("\nAuto input file path?y/n\n")
        if flag4 == "" or flag4 == "y" or flag4 == "Y":
            _,_,f = findAllFiles(os.getcwd(),".md")
            file_path  = f[0]
        else:
            file_path = raw_input("Input the file path:\n")
        out_res = file_path.split('.')[-2] + "_auto.md"
        shutil.copyfile(file_path,out_res)
        return out_res
    else:
        # 第二步，根据规则创建新的文件名
        start = raw_input("Input the start index of images(0 as default):\n")
        if start == "":
            start = "0"
        new = generateFormatName(ori, int(start))

        # 第三步，文件批量改名
        renameImages(ori, new)

        flag1 = raw_input("Resize all images?y/[n]\n")
        if  flag1 == "y" or flag1 == "Y":
            # 第四步，批量修改文件大小并替换原图
            saveImages(new)

        flag2 = raw_input("Tinify all images?[y]/n\n")
        if flag2 == "" or flag2 == "y" or flag2 == "Y":
            # 第五步，调用TinyPNG接口进行图像压缩，并替换原图
            tinifyImage(new)

        flag3 = raw_input("Auto insert tags into files?[y]/n\n")
        if flag3 == "" or flag3 == "y" or flag3 == "Y":
            # 第六步，生成每个文件对应的img标签并自动插入
            # 注意文件名不支持中文
            flag4 = raw_input("\nAuto input file path?[y]/n\n")
            if flag4 == "" or flag4 == "y" or flag4 == "Y":
                _,_,f = findAllFiles(os.getcwd(),".md")
                file_path  = f[0]
            else:
                file_path = raw_input("Input the file path:\n")
            insertImgTag(html_part1, html_part2, html_part3, new, file_path)
            out_res = file_path.split('.')[-2] + "_auto.md"
            print("Success format images!")
            return out_res
        else:
            # 第六步，生成每个文件对应的img标签
            generateHTML(html_part1, html_part2, html_part3, new, root_dir)

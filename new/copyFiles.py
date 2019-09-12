# coding=utf-8
import shutil
import os

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

def findAllImages(root_dir):

    separator = os.path.sep
    paths = []
    names = []
    files = []
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".PNG") or filename.endswith(".JPG") or filename.endswith(".gif") or filename.endswith(".GIF") or filename.endswith(".mp4") or filename.endswith(".MP4") or filename.endswith(".avi") or filename.endswith(".AVI"):
                paths.append(parent + separator)
                names.append(filename)
    for i in range(paths.__len__()):
        files.append(paths[i] + names[i])
    paths.sort()
    names.sort()
    files.sort()
    return paths, names, files

def execCopyFiles():

    flag1 = raw_input("\nAuto input blog root path?[y]/n\n")
    if flag1 == "" or flag1 == "y" or flag1 == "Y":
        root_path = "F:\\zhaoxuhui.github.io\\"
    else:
        root_path = raw_input("Input root path of blog:\n")+os.sep

    img_path = os.getcwd()+os.sep+"imgs"+os.sep
    img_target_path = root_path+"assets\\images\\blog\\content\\"
    post_target_path = root_path+"_posts\\"
    
    # 剪贴图片
    _,img_names,img_files = findAllImages(img_path)
    for i in range(len(img_files)):
        shutil.copyfile(img_files[i],img_target_path+img_names[i])
    for i in range(len(img_files)):
        os.remove(img_files[i])
    
    # 剪贴博客
    _,n,_= findAllFiles(".","_toc.md")
    if len(n)==0:
        print("can't find right file.")
        exit()
    file_name = n[0][:-7]+".md"
    shutil.copyfile(n[0],post_target_path+file_name)
    os.remove(n[0])

    # 删除其它md文件
    _,_,f= findAllFiles(".",".md")
    for item in f:
        os.remove(item)
    print("Success copy files!")
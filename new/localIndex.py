# coding=utf-8
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


def splitName(name):
    year = name[:4]
    month = name[5:7]
    day = name[8:10]
    title = name[11:].split(".")[0]
    url = year + "/" + month + "/" + day + "/" + title
    return url

def execIndex():
    flag1 = raw_input("\nAuto input blog root path?[y]/n\n")
    if flag1 == "" or flag1 == "y" or flag1 == "Y":
        root_path = "F:\\zhaoxuhui.github.io\\"
    else:
        root_path = raw_input("Input root path of blog:\n")+os.sep

    # 先找到已有的所有博客
    _, names, _ = findAllFiles(root_path+"_posts", "")
    urls = []
    for item in names:
        urls.append(splitName(item))

    # 再将新的放进去，由于在这一步还并没有把md文件拷贝到_posts文件夹下，所以需要手动加上
    flag2 = raw_input("Auto input post file name?[y]/n\n")
    if flag2 == "" or flag2 == "y" or flag2 == "Y":
        _,n,_= findAllFiles(".","_toc.md")
        if len(n)==0:
            print("can't find right file.")
            exit()
        file_name = n[0][:-7]
    else:
        name = raw_input("Input file name:\n")
        file_name = name.split("\\")[-1].split(".")[0]
    file_name = splitName(file_name)
    urls.append(file_name)

    f = open(root_path+"posts.idx", 'w')
    f.write(len(urls).__str__() + "\n")
    for item in urls:
        f.write(item + "\n")
    f.close()
    print("Success generate posts.idx!")
   
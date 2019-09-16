# coding=utf-8
import os
import chardet
import sys


def getEncoding(str):
    if type(str) is unicode:
        print 'unicode'
    else:
        print chardet.detect(str)


def findAllFiles(root_dir, filter):
    """
    在指定目录查找指定类型文件

    :param root_dir: 查找目录
    :param filter: 文件类型
    :return: 路径、名称、文件全路径

    """

    uni_root_dir = root_dir.decode('gbk')
    uni_filter = filter.decode('gbk')

    separator = os.path.sep
    paths = []
    names = []
    files = []
    for parent, dirname, filenames in os.walk(uni_root_dir):
        for filename in filenames:
            if filename.endswith(uni_filter):
                paths.append((parent + separator))
                names.append(filename)
    for i in range(paths.__len__()):
        files.append(paths[i] + names[i])
    paths.sort()
    names.sort()
    files.sort()
    return paths, names, files


def replaceDunHao(string, replace):
    if string.__contains__(u'、'):
        dun = string.find(u'、')
        # 对于utf8字符串，顿号是中文字符，占4个字节，所以加3
        # 对于unicode字符串，直接+1即可
        string = string[:dun] + replace + string[dun + 1:]
        return string


def replaceSharp(string, replace):
    if string.__contains__(u'#'):
        sharp = string.find(u'#')
        string = string[:sharp] + replace + string[sharp + 1:]
        return string


def replaceSpace(string, replace):
    if string.__contains__(u' '):
        space = string.find(u' ')
        string = string[:space] + replace + string[space + 1:]
        return string


def replaceColon(string, replace):
    if string.__contains__(u'：'):
        colon = string.find(u'：')
        string = string[:colon] + replace + string[colon + 1:]
        return string


def getLink(string):
    res = string
    # getEncoding(res)
    while res.__contains__(u'、'):
        res = replaceDunHao(res, u'-')
    while res.__contains__(u'#'):
        res = replaceSharp(res, u'-')
    while res.__contains__(u' '):
        res = replaceSpace(res, u'-')
    while res.__contains__(u'：'):
        res = replaceColon(res, u'-')
    return res


def splitName(name):
    year = name[:4]
    month = name[5:7]
    day = name[8:10]
    title = name[11:].split(".")[0]
    title_link = getLink(title)
    url = year + "/" + month + "/" + day + "/" + title_link
    return url


def execIndex():
    flag1 = raw_input("\nAuto input blog root path?[y]/n\n")
    if flag1 == "" or flag1 == "y" or flag1 == "Y":
        root_path = "F:\\zhaoxuhui.github.io\\"
    else:
        root_path = raw_input("Input root path of blog:\n") + os.sep

    # 先找到已有的所有博客
    _, names, _ = findAllFiles(root_path + "_posts", "")
    urls = []
    for item in names:
        urls.append(splitName(item))

    # 再将新的放进去，由于在这一步还并没有把md文件拷贝到_posts文件夹下，所以需要手动加上
    flag2 = raw_input("Auto input post file name?[y]/n\n")
    if flag2 == "" or flag2 == "y" or flag2 == "Y":
        _, n, _ = findAllFiles(".", "_toc.md")
        if len(n) == 0:
            flag3 = raw_input("Can't find right file,update existed file?[y]/n")
            if flag3 == "" or flag3 == "y" or flag3 == "Y":
                pass
            else:
                print("exit program.")
                exit()
        else:
            file_name = n[0][:-7]
            urls.append(file_name)
    else:
        name = raw_input("Input file name:\n")
        file_name = name.split("\\")[-1].split(".")[0]
        file_name = splitName(file_name)
        urls.append(file_name)

    f = open(root_path + "posts.idx", 'w')
    f.write(len(urls).__str__() + "\n")
    for item in urls:
        f.write(item.encode('gbk') + "\n")
    f.close()
    print("Success generate posts.idx!")
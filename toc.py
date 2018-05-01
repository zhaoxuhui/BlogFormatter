-  # coding=utf-8


def deleteLeftParentheses(string):
    if string.__contains__('('):
        left_col = string.find('(')
        string = string[:left_col] + string[left_col + 1:]
        return string


def deleteRightParentheses(string):
    if string.__contains__(')'):
        right_col = string.find(')')
        string = string[:right_col] + string[right_col + 1:]
        return string


def deleteDot(string):
    if string.__contains__('.'):
        dot = string.find('.')
        string = string[:dot] + string[dot + 1:]
        return string


def deleteSingleQuoteMark(string):
    if string.__contains__('`'):
        pie = string.find('`')
        string = string[:pie] + string[pie + 1:]
        return string


def deleteLeftDoubleQuoteMark(string):
    if string.__contains__('“'):
        left_double = string.find('“')
        string = string[:left_double] + string[left_double + 3:]
        return string


def deleteRightDoubleQuoteMark(string):
    if string.__contains__('”'):
        right_double = string.find('”')
        string = string[:right_double] + string[right_double + 3:]
        return string


def deleteDunHao(string):
    if string.__contains__('、'):
        dun = string.find('、')
        string = string[:dun] + string[dun + 3:]
        return string


def deleteLeftBracket(string):
    if string.__contains__('['):
        left_bracket = string.find('[')
        string = string[:left_bracket] + string[left_bracket + 1:]
        return string


def deleteRightBracket(string):
    if string.__contains__(']'):
        right_bracket = string.find(']')
        string = string[:right_bracket] + string[right_bracket + 1:]
        return string


def deleteAdd(string):
    if string.__contains__('+'):
        add_plus = string.find('+')
        string = string[:add_plus] + string[add_plus + 1:]
        return string


def deleteAnd(string):
    if string.__contains__('&'):
        And = string.find('&')
        string = string[:And] + string[And + 1:]
        return string


def replaceDunHao(string, replace):
    if string.__contains__('、'):
        dun = string.find('、')
        # 顿号是中文字符，占4个字节，所以加3
        string = string[:dun] + replace + string[dun + 3:]
        return string


def replaceSharp(string, replace):
    if string.__contains__('#'):
        sharp = string.find('#')
        string = string[:sharp] + replace + string[sharp + 1:]
        return string


def replaceSpace(string, replace):
    if string.__contains__(' '):
        space = string.find(' ')
        string = string[:space] + replace + string[space + 1:]
        return string


def replaceColon(string, replace):
    if string.__contains__('：'):
        colon = string.find('：')
        string = string[:colon] + replace + string[colon + 3:]
        return string


def getTitle(raw_str):
    # 1.分离#与标题内容，并确定标题等级
    res = raw_str.split(' ')
    level = res[0].count('#')
    # 重新拼接标题内容，解决包含标题中包含多个空格时获取的标题内容不全的问题
    title = ""
    for i in range(1, res.__len__()):
        # 解决重新拼接标题时，标题内的空格被删掉的问题
        title = title + " " + res[i]
    # 去除标题行首的空格
    title = title.lstrip()
    # 去除标题行尾的换行
    title = title.strip('\n')
    title_for_show = title

    # 2.删除特殊字符
    while title.__contains__('.'):
        title = deleteDot(title)
    while title.__contains__('('):
        title = deleteLeftParentheses(title)
    while title.__contains__(')'):
        title = deleteRightParentheses(title)
    while title.__contains__('`'):
        title = deleteSingleQuoteMark(title)
    while title.__contains__('、'):
        title = deleteDunHao(title)
    while title.__contains__('“'):
        title = deleteLeftDoubleQuoteMark(title)
    while title.__contains__('”'):
        title = deleteRightDoubleQuoteMark(title)
    while title.__contains__('['):
        title = deleteLeftBracket(title)
        # print(title)
    while title.__contains__(']'):
        title = deleteRightBracket(title)
    while title.__contains__('+'):
        title = deleteAdd(title)
    while title.__contains__('&'):
        title = deleteAnd(title)
    while title.__contains__(' '):
        title = replaceSpace(title, '-')

    # 3.英文大写变小写
    res = title.lower()

    return level, title_for_show, res


def getLink(base, string):
    while string.__contains__('、'):
        string = replaceDunHao(string, '-')
    while string.__contains__('#'):
        string = replaceSharp(string, '-')
    while string.__contains__(' '):
        string = replaceSpace(string, '-')
    while string.__contains__('：'):
        string = replaceColon(string, '-')
    return base + "#" + string


def getBase(year, month, day, filename, part):
    res = part + "/" + year + "/" + month + "/" + day + "/" + filename + ".html"
    while res.__contains__('、'):
        res = replaceDunHao(strresing, '-')
    while res.__contains__('#'):
        res = replaceSharp(res, '-')
    while res.__contains__(' '):
        res = replaceSpace(res, '-')
    while res.__contains__('：'):
        res = replaceColon(res, '-')
    return res


def splitInfo(file_path):
    # 文件名有固定的格式，xxxx-xx-xx-xxxxx.md
    index = file_path.rfind('\\')
    filename = file_path[index + 1:]
    temp = filename.split('-')
    year = temp[0]
    month = temp[1]
    day = temp[2]
    filename = temp[3].split('.')[0]
    return year, month, day, filename


def generateTOC(level, content):
    if level == 0:
        content = "- " + content
    elif level == 1:
        content = "\t- " + content
    elif level == 2:
        content = "\t\t- " + content
    elif level == 3:
        content = "\t\t\t- " + content
    elif level == 4:
        content = "\t\t\t\t- " + content
    elif level == 5:
        content = "\t\t\t\t\t- " + content
    elif level == 6:
        content = "\t\t\t\t\t\t- " + content
    return content


def execFunction(input_path):
    # 博客网址的共有部分，可以替换成你自己的
    part = "http://zhaoxuhui.top/blog"

    # 判断手动输入还是自动传入
    flag = raw_input("Auto insert?y/n\n")
    if flag == "y":
        path = input_path
    else:
        path = raw_input("Input path of file:\n")

    # 利用decode函数解决文件名中含有中文字符的问题
    f = open(path.decode('utf8'), 'r')
    headers = []
    lines = []
    line = f.readline()
    lines.append(line)
    while line:
        line = f.readline()
        lines.append(line)
        # 通过每一行中含有的井号数量计算，因为在博客中一般不采用一、二级标题(太大了)
        # 不好看，所以认为如果一行之中包含有连续两个井号，就认为是标题
        if line.__contains__("##"):
            headers.append(line.decode('utf-8').encode('utf-8'))
    f.close()
    # 如果没找到标题，程序退出
    if headers.__len__() == 0:
        print("No title.")
        exit()

    # 获取除去`_auto`后缀的正确的名字
    correct_path = input_path[:-8] + ".md"
    year, month, day, name = splitInfo(correct_path)
    base = getBase(year, month, day, name, part)

    formatted_title = []
    links = []
    bookmarks = []
    format_mark = []
    levels = []
    for item in headers:
        # 获取标题对应的id
        lev, show, res = getTitle(item)
        formatted_title.append(res)
        # 由每一篇博客的网址和标题id信息拼接url
        link = getLink(base, res)
        links.append(link)
        levels.append(lev)
        # 拼接Markdown格式的超链接
        content = "[" + show + "](" + link + ")"
        bookmarks.append(content)

    # 寻找标题最大等级(数字最小)，以此作为一级列表
    # 因为在博客中很多都是直接从3级甚至4级标题开始的
    # 因此没必要空出来1、2级标题的层次，非常难看，直接把3或4当作第一级
    min_level = (min(levels))
    for i in range(levels.__len__()):
        levels[i] = levels[i] - min_level

    # 基于标题不同等级，按照Markdown语法生成TOC
    for i in range(bookmarks.__len__()):
        format_mark.append(generateTOC(levels[i], bookmarks[i]))

    new_lines = []
    # 按照我自己的post格式，将TOC插入在前12行之后
    for i in range(12):
        new_lines.append(lines[i])
    # 写入TOC
    for item in format_mark:
        new_lines.append(item + "\n")
    # 添加TOC与正文之间的分隔线
    new_lines.append("<hr style=\"margin:0em 0em 1.75em 0em;\">\n")
    # 与博客配套的自定义的目录与正文的分隔符
    new_lines.append("<!--break-->")
    # 写入正文剩余部分内容
    for i in range(11, lines.__len__()):
        new_lines.append(lines[i])

    # 将重新生成的post内容输出到md文件中，覆盖原文件
    out_toc = ""
    for item in new_lines:
        out_toc = out_toc + item
    path = correct_path[:-3] + "_toc.md"
    fout = open(path.decode('utf8'), 'w')
    fout.writelines(out_toc)
    fout.close()

    print("Success!")

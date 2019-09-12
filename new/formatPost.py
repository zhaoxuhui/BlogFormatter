# coding =utf-8
import toc
import BlogImages
import localIndex
import copyFiles

flag0 = raw_input("Generate formatted images?[y]/n\n")
out_res = ""
if flag0 == "" or flag0 == "y" or flag0 == "Y":
    print("Format images...\n")
    out_res = BlogImages.execImgs()

flag1 = raw_input("\nInsert TOC?[y]/n\n")
if flag1 == "" or flag1 == "y" or flag1 == "Y":
    print("\nInsert TOC...\n")
    toc.execFunction(out_res)

flag2 = raw_input("\nGenerate posts.idx?[y]/n\n")
if flag2 == "" or flag2 == "y" or flag2 == "Y":
    print("\nGenerate posts.idx...\n")
    localIndex.execIndex()

flag3 = raw_input("\nCopy files?[y]/n\n")
if flag3 == "" or flag3 == "y" or flag3 == "Y":
    print("\nCopy files...\n")
    copyFiles.execCopyFiles()
else:
    print("Something went wrong,please check.")
    exit()
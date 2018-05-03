import toc
import BlogImages

flag0 = raw_input("Auto generate IMG?y/n\n")
out_res = ""
if flag0 == "y":
    print("Format images...\n")
    out_res = BlogImages.execImgs()

flag1 = raw_input("\nInsert TOC?y/n\n")
if flag1 == "y":
    print("\nInsert TOC...\n")
    toc.execFunction(out_res)
else:
    exit()

# coding=utf-8
import os
from tkinter import filedialog
from tkinter import Tk

def findtxt(path, ret):
    filelist = os.listdir(path)
    filelist.sort(key=lambda x: int(x.split('.')[0]))  # 对文件列表进行排序，按照文件名（不包括扩展名）转换为整数的结果排序
    for filename in filelist:
        de_path = os.path.join(path, filename)
        if os.path.isfile(de_path):
            if de_path.endswith(".txt"):
                ret.append(de_path)
        else:
            findtxt(de_path, ret)


if __name__ == "__main__":
    ret = []

    # 创建Tk root
    root = Tk()
    # 隐藏主窗口
    root.withdraw()

    # 打开选择文件夹对话框
    filedir = filedialog.askdirectory(title='选择文件夹')
    findtxt(filedir, ret)

    output_file = filedialog.asksaveasfilename(defaultextension=".txt", title='选择输出文件')
    for ret_ in ret:
        with open(output_file, 'a', encoding="utf-8") as f:
            with open(ret_, encoding="utf-8") as fp:
                for line in fp:
                    # line = str(line).replace("\n", "")  # 去换行符
                    f.write(line)
                f.write('\n')

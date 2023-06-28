# auth ： xiaokou
# date ： 2023/6/28 11:34

# 在后台随机生成10个16位的随机激活码
import random
import sys
import tkinter.messagebox

activation_codes = [str(random.randint(1e15,1e16-1)) for i in range (10)]
print(activation_codes)

def check_activation_code(code):
    if code in activation_codes:
        tkinter.messagebox.showinfo(title='激活成功',message='软件已成功激活')
        return True
    else:
        tkinter.messagebox.showinfo(title='激活失败',message='无效激活码,软件将退出')
        sys.exit()
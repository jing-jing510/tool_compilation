# auth ： xiaokou
# date ： 2023/6/28 11:00
import tkinter as tk
from tkinter import ttk
import activation
import openai_text
# 创建主窗口
root = tk.Tk()
root.title("文本转换")
root.geometry("1280x1080")
# 第一行:软件激活码
label_activation = tk.Label(root, text="这是后台程序，还暂时不收到激楚码:")
label_activation.grid(row=0, column=0)
entry_activation = tk.Entry(root)
entry_activation.grid(row=0, column=1)
button_activation = tk.Button(root, text="激活软件", command=lambda: activation.check_activation_code(entry_activation.get()))
button_activation.grid(row=0, column=2)
#第一行:GPT端口
label_port =tk.Label(root, text="GPT端口:")
label_port.grid(row=0, column=3)
port_list = ['gpt-3.5-turbo','gpt-4.0-turbo']
port_variable = tk.StringVar(root)
port_variable.set(port_list[0]) # 默认值
optionmenu_port = tk.OptionMenu(root, port_variable, *port_list)
optionmenu_port.grid(row=0, column=4)
# 第一行：GPT key
# label_key = tk.Label(root, text="GPT_key:")
# label_key.grid(row=0, column=5)
# entry_key = tk.Entry(root)
# entry_key.grid(row=0, column=6)
# button_set_gpt_key = tk.Button(root, text="设置GPT Key", command=lambda: openai_text.set_gpt_key(entry_gpt_key.get()))
# button_set_gpt_key.grid(row=0, column=7)
# 创建一个按钮,执行openai_text.ai_fenjing_array() 操作,将其数组lines 放到表格当中
button_ai_fenjing_array = tk.Button(root, text="AI分镜数组", command=lambda: openai_text.ai_fenjing_array(port_variable.get()))
# 创建一个表格 第一行 原文 第二行 分镜 第三行 正向关键词 第四行 反向关键词 第五行 图片
# 创建表格
table = ttk.Treeview(root)
table["columns"] = ("Original", "Fenjing", "Positive", "Negative", "Image")
# 设置表头
table.heading("Original", text="原文")
table.heading("Fenjing", text="分镜")
table.heading("Positive", text="正向关键词")
table.heading("Negative", text="反向关键词")
table.heading("Image", text="图片")
# 添加表格到界面
table.grid(row=1, column=0, columnspan=5, padx=10, pady=10)


# 运行主循环，显示窗口
root.mainloop()
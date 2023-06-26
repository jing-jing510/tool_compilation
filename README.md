# tool_compilation

各类小工具合集

# txt文本整合

功能：将一个文件夹里所有的txt 按照顺序进行整合到一个txt文件当中

文本1：1girl, blue eyes, solo, black hair, food, shirt, chinese text, long hair, looking at viewer, white shirt, korean text, noodles, bowl, ramen, collarbone, window, indoors, short sleeves

文本2：1girl, blue eyes, food, solo, black hair, long hair, chinese text, shirt, noodles, looking at viewer, korean text, white shirt, chair, bowl, window, ramen, indoors, collarbone, sitting, table

合并后：1girl, blue eyes, solo, black hair, food, shirt, chinese text, long hair, looking at viewer, white shirt, korean text, noodles, bowl, ramen, collarbone, window, indoors, short sleeves
1girl, blue eyes, food, solo, black hair, long hair, chinese text, shirt, noodles, looking at viewer, korean text, white shirt, chair, bowl, window, ramen, indoors, collarbone, sitting, table

---

在这个任务中，我们实际上涉及到的知识点主要有以下几个：

1. **Python的文件操作**：Python中通过内置的 `open()`函数来读取和写入文件，同时使用 `os`模块来处理文件和目录的路径。
2. **Python的递归函数**：在搜索文件夹及其子文件夹中的文件时，使用了递归的概念。在函数 `findtxt`中，当发现一个子目录时，函数会调用自身来查找该子目录中的文件。
3. **Python的排序**：使用Python的内置函数 `sort()`和 `lambda`匿名函数对文件列表进行排序。`lambda`函数用于定义排序的关键字。
4. **Python-docx模块**：该模块是用于读取、查询和修改Microsoft Word 2007/2010文档的Python库。在这个任务中，我们使用Python-docx模块读取Word文档的内容，并创建一个新的文档。
5. **PyInstaller**：PyInstaller是一个将Python应用程序转换成独立的可执行文件的工具，使得没有安装Python环境的用户也可以运行Python程序。
6. **tkinter模块**：tkinter是Python的标准GUI库。Python使用tkinter可以快速的创建GUI应用程序。在这里我们使用它创建一个文件对话框，让用户选择输入和输出的文件。
7. **Python的字符串操作**：在处理每一行的文本时，我们使用Python的字符串函数，如 `strip()`、`startswith()`和 `split()`，来删除不需要的空白字符、检查行的开始和划分行。

以上就是这个任务涉及到的主要知识点。

# Word考题合并一行

功能：将word考题当中

1. 葡萄糖分子进入小肠上皮刷状缘时是

A. 单纯扩散

B. 易化扩散

C. 原发性主动转运

D. 继发性主动转运

正确答案：D

2. 下列关于骨骼肌收缩耦联叙述正确的是

A. 纵管将电兴奋传入肌细胞深部

B. 肌膜和横管膜L 型钙通道激活

C. 终池内Ca2+ 逆浓度差进入胞质

D.Ca2+ 与肌动蛋白钙结合亚基结合

正确答案：B

这样的形式变成

1. 葡萄糖分子进入小肠上皮刷状缘时是 A. 单纯扩散 B. 易化扩散 C. 原发性主动转运 D. 继发性主动转运 正确答案：D
2. 下列关于骨骼肌收缩耦联叙述正确的是 A. 纵管将电兴奋传入肌细胞深部 B. 肌膜和横管膜L 型钙通道激活 C. 终池内Ca2+ 逆浓度差进入胞质 D.Ca2+ 与肌动蛋白钙结合亚基结合 正确答案：B

---

知识点：

1. **Python的文件操作**：我们使用了`os`模块来列出目录中的文件，使用`open`函数来读取和写入文件。
2. **Python中的文本处理**：我们使用了字符串的`split`、`strip`方法和`+`运算符来处理文本。我们还用到了正则表达式库`re`来匹配和处理字符串。
3. **Python操作Word文件**：我们使用了`python-docx`库来读取和写入Word (.docx) 文件。我们读取了文档中的段落，对段落进行处理后，创建了一个新的文档并保存。
4. **Python命令行参数解析**：我们使用了`argparse`库来解析命令行参数，使得我们的脚本可以接受用户输入的文件路径。
5. **创建Python脚本和可执行文件**：我们使用`pyinstaller`将Python脚本打包成了可执行文件，使得没有Python环境的用户也可以使用我们的脚本。
6. **Python创建GUI应用**：我们使用了`tkinter`库来创建一个简单的图形用户界面，让用户可以通过图形界面来选择文件，而不仅仅是通过命令行参数。

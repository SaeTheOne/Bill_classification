# 方便将支付宝和微信的账单进行分类后导入记账app
## 使用方法
1.安装Python环境  
2.下载main.py和classification.py两个文件  
3.运行**main.py**，选择存放从支付宝和微信导出的账单的文件夹  
4.完成后会有一个完成的文件夹生成在账单的文件夹内，里面的sc.xlxs就是分类好的文件  

**如果需要修改一级分类和二级名称，在classification.py中修改就好，我将>20元的三餐变成了大餐，如果不需要将那段代码注释掉就行**

使用到的库csv、 glob、 tkinter、 re、 openpyxl、 spire.xls

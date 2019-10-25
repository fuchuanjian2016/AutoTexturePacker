import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter.filedialog import askdirectory
import tkinter.messagebox  # 要使用messagebox先要导入模块
import os
import sys;


#sys.setdefaultencoding('utf8')

window = tk.Tk()
 
# 给窗口的可视化起名字
window.title('P6-UI贴图打包工具 deta')
window.resizable(False, False)
 
# 设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x

# 参数
path = tk.StringVar(); # 散图路径
outPath = tk.StringVar(); # 打包好的文件路径
picWidth = tk.StringVar(); # 贴图尺寸px width
picHeight = tk.StringVar(); # 贴图尺寸px height
savedFile = ".ini"

def judge2(num):
    result = num & (num-1)
    if result == 0:
        return True
    else:
        return False

def showMsg(txt):
	tkinter.messagebox.showinfo(title='消息',message=txt) 

# 路径选择函数
def selectPath():
    p = askdirectory()
    path.set(p)

# 打包路径选择函数
def selectOutPath():
    p = askdirectory()
    outPath.set(p)   

# 打包路径选择函数
def onClickCreate():
	if path.get() == "":
		showMsg("散图路径不能为空")
		return
	elif outPath.get() == "":
		showMsg("生成路径不能为空")
		return
	elif picWidth.get() == "" or picHeight.get() == "" :
		showMsg("贴图尺寸不能为空")
		return

	if (int(picWidth.get()) == 0 ) or (int(picHeight.get() == 0)):
		showMsg("贴图尺寸不能为0")
		return

	if not judge2(int(picWidth.get())) :
		showMsg("贴图尺寸必须是2的次幂")
		return
	if not judge2(int(picHeight.get())) :
		showMsg("贴图尺寸必须是2的次幂")
		return
	# 执行命令
	pathStr = path.get()
	outPathStr = outPath.get();
	width = picWidth.get()
	height = picHeight.get();
	#cmd = "TexturePacker {pathStr} {outPathStr} --sheet out.png --data out.plist --allow-free-size --no-trim —-max-width {width} —-max-height {height} --format cocos2d";
	#cmd = cmd.format(pathStr=pathStr, outPathStr=outPathStr, width = width, height = height)
	cmd = "python BuildTps.py {pathStr} {outPathStr}"
	cmd = cmd.format(dir=os.getcwd(), pathStr=pathStr, outPathStr=outPathStr)
	os.system(cmd);
	saveConfig();

	showMsg("生成成功 " + outPath.get())

def readSaved():
	if os.path.exists(savedFile):
		with open(savedFile, 'r') as f:
		    lines = f.read().splitlines()
		    line_num = len(lines)
		    if line_num == 4:
			    path.set(lines[0])
			    outPath.set(lines[1])
			    picWidth.set(lines[2])
			    picHeight.set(lines[3])

def saveConfig():
	save_data = [ path.get(), outPath.get(), picWidth.get(), picHeight.get() ];
	with open(savedFile, mode='w',encoding='utf-8') as f:
 		for line in save_data:    
   			f.write(line)
   			f.write('\n')

readSaved();

poxX = 20
posY = 50

# 散图路径
tk.Button(window,text = "散图路径", command = selectPath).place(x=poxX, y=posY)
tk.Entry(window, textvariable = path, width= 40).place(x=poxX + 100, y=posY - 4)

posY = 100
# 生成路径
tk.Button(window,text = "生成路径", command = selectOutPath).place(x=poxX, y=posY)
tk.Entry(window, textvariable = outPath, width= 40).place(x=poxX + 100, y=posY - 4)


posY = 150
# 生存路径
tk.Label(window,text = "贴图尺寸").place(x=poxX, y=posY)
tk.Entry(window, textvariable = picWidth, width= 5).place(x=poxX + 100, y=posY - 4)
tk.Label(window,text = "px").place(x=poxX + 160, y=posY)
tk.Label(window,text = "width").place(x=poxX + 100, y=posY+25)

tk.Entry(window, textvariable = picHeight, width= 5).place(x=poxX + 250, y=posY - 4)
tk.Label(window,text = "px").place(x=poxX + 310, y=posY)
tk.Label(window,text = "width").place(x=poxX + 250, y=posY+25)

# 生成精灵
tk.Button(window,text = "生成精灵", command = onClickCreate, fg='green',font=('Arial', 25)).place(x=180, y=230)



window.mainloop()


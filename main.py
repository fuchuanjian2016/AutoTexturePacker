  # -*- coding: utf-8 -*
import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter.filedialog import askdirectory
import tkinter.messagebox  # 要使用messagebox先要导入模块
import os
import sys;

import os, shutil, json
import subprocess
import io
import sys
import re
import hashlib
import collections
#sys.setdefaultencoding('utf8')

################################## build tool start  ########################################
class BuildTps:
    def __init__(self, sourcePath, resPath, width, height):
        self.dir = os.path.split(os.path.realpath(__file__))[0]
        self.sourcePath = sourcePath
        self.resPath = resPath
        self.resFileName = os.path.split(os.path.split(self.resPath)[0])[1]
        self.tempPath = self.dir+"/tmp/"
        self.folderList = []
        self.width = width
        self.height = height
    def build(self):
        if os.path.exists(self.tempPath):
            shutil.rmtree(self.tempPath)

        self.generateFileList()
        for index,folder in enumerate(self.folderList):
            self.buildFolderTps(folder, index+1)

    # 目录拷贝函数
    def dir_copyFolder(self, src, dst):
        names = os.listdir(src)
        # 目标文件夹不存在，则新建
        if not os.path.exists(dst):
            os.makedirs(dst)
        # 遍历源文件夹中的文件与文件夹
        for name in names:
            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            try:
                # 是文件夹则递归调用本拷贝函数，否则直接拷贝文件
                if not os.path.isdir(srcname):
                    if (not os.path.exists(dstname)
                        or ((os.path.exists(dstname))
                            and (os.path.getsize(dstname) != os.path.getsize(srcname)))):
                        shutil.copy(srcname, dst)
            except:
                error.traceback();
                raise

   
    def generateFileList(self):
        print("generateFileList "+ self.sourcePath)       
        if self.checkFolderCanTps(self.sourcePath):
            self.folderList.append(self.sourcePath)
        print("[Success] ")

    def checkFolderCanTps(self, folder):
        print("checkFolderCanTps "+ folder)  
        fileList = os.listdir(folder)#列出目录下的所有文件和目录
        for fileName in fileList:
            filePath = os.path.join(folder,fileName)
            if not os.path.isdir(filePath):
                if fileName[0:1] != ".":
                    return True
        return False

    def buildFolderTps(self,folderPath,index):
        print("--------------------------")
        print ("sourcePath "+self.sourcePath)
        if folderPath.find('\\') > 0:
        	folderNameArr = folderPath.split('\\')
        else:
        	folderNameArr = folderPath.split('/')
        folderName = folderNameArr[len(folderNameArr)-1]
        print("folderPath "+ folderPath)
        print ("folderName "+ folderName)

        folderRelativePath = folderPath[len(self.sourcePath):]
        print("folderRelativePath "+ folderRelativePath)
        resRelativePath = self.resFileName+"/" + folderRelativePath
        print("resRelativePath "+ resRelativePath)
        targetBasePath = self.tempPath + "project"+str(index)+"/"
        targetFolderPath = targetBasePath + "/folder/" + folderRelativePath

        print ("targetBasePath "+ targetBasePath)
        print ("targetFolderPath "+ targetFolderPath)
        self.dir_copyFolder(folderPath, targetFolderPath)

        FileSize = sum([len(x) for _, _, x in os.walk(os.path.dirname(targetFolderPath))])
        
        #替换模板
        tpsHandle = open("template.tps")
        print("Size == 1")

        
        tpsContent = tpsHandle.read()
        tpsHandle.close()
        tpsContent = tpsContent.replace('{textureFileName}', folderName + "{n}.png")
        tpsContent = tpsContent.replace('{dataFileName}', folderName + "{n}.paper2dsprites")
        # if FileSize > 1:
        #     tpsContent = tpsContent.replace('{textureFileName}', folderName + "{n}.png")
        #     tpsContent = tpsContent.replace('{dataFileName}', folderName + "{n}.paper2dsprites")
        #     tpsContent = tpsContent.replace('{Param_extrude}', "0")
        #     tpsContent = tpsContent.replace('{Param_Margin}', "0")
        # else:
        #     tpsContent = tpsContent.replace('{textureFileName}', folderName + ".png")
        #     tpsContent = tpsContent.replace('{dataFileName}', folderName + ".paper2dsprites")
        #     tpsContent = tpsContent.replace('{Param_extrude}', "0")
        #     tpsContent = tpsContent.replace('{Param_Margin}', "0")
            
        tpsContent = tpsContent.replace('{filename}',"folder")
        tpsContent = tpsContent.replace('{maxSizeWidth}',self.width)
        tpsContent = tpsContent.replace('{maxSizeHeight}',self.height)
        TPSPath = targetBasePath + folderName + ".tps"
        print ("TPSPath "+ TPSPath)
        try:
        	open(TPSPath, "w").write(tpsContent)
        except IOError:
        	tkinter.messagebox.showinfo(title='错误',message="路径无效"+TPSPath)
        	return
        

     
        #shutil.copy(folderPath, self.resPath + )
        CMD = 'texturePacker ' + targetBasePath + folderName + ".tps"
        print("+++++++++++++++++++++")
        result=os.system(CMD)

        if result!=0:
            tkinter.messagebox.showinfo(title='错误',message="生成失败，报错信息请查看控制台") 
        else:
            tkinter.messagebox.showinfo(title='成功',message="生成成功 "+ self.resPath)

        #plistHandle = open(targetBasePath + folderName + ".paper2dsprites")
        #plistContent = plistHandle.read()
        #plistHandle.close()

        targetResFolderPath = self.resPath + folderRelativePath + "/"


        if os.path.exists(targetResFolderPath):
            shutil.rmtree(targetResFolderPath)

        #plistContent = re.sub('\$TexturePacker:.*\$', 'lede', plistContent)
        #open(targetResFolderPath +  folderName + ".paper2dsprites", "w").write(plistContent)

       
        #shutil.copytree(targetBasePath + folderName + ".png", targetResFolderPath + folderName + ".png")


        shutil.copytree(targetBasePath, targetResFolderPath, ignore=shutil.ignore_patterns('*.tps', 'folder'))

        if os.path.exists(self.tempPath):
            shutil.rmtree(self.tempPath)

    def run(self):
        os.chdir(self.dir)
        self.build()

################################## build tool end  ########################################

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
	#cmd = "python BuildTps.py {pathStr} {outPathStr}"
	#cmd = cmd.format(dir=os.getcwd(), pathStr=pathStr, outPathStr=outPathStr)
	#os.system(cmd);
	saveConfig();

	buildTps = BuildTps(pathStr, outPathStr, width, height)
	buildTps.run()

	# 检测生成是否成功

	#showMsg("生成成功 " + outPath.get())

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
posY = 60

# 散图路径
tk.Button(window,text = "散图路径", command = selectPath).place(x=poxX, y=posY)
tk.Entry(window, textvariable = path, width= 40).place(x=poxX + 100, y=posY - 4)

posY = 100
# 生成路径
tk.Button(window,text = "生成路径", command = selectOutPath).place(x=poxX, y=posY)
tk.Entry(window, textvariable = outPath, width= 40).place(x=poxX + 100, y=posY - 4)


posY = 160
# 生存路径
tk.Label(window,text = "贴图尺寸").place(x=poxX, y=posY)
tk.Entry(window, textvariable = picWidth, width= 5).place(x=poxX + 100, y=posY - 4)
tk.Label(window,text = "px").place(x=poxX + 160, y=posY)
tk.Label(window,text = "width").place(x=poxX + 100, y=posY+25)

tk.Entry(window, textvariable = picHeight, width= 5).place(x=poxX + 250, y=posY - 4)
tk.Label(window,text = "px").place(x=poxX + 310, y=posY)
tk.Label(window,text = "height").place(x=poxX + 250, y=posY+25)

tk.Label(window,text = "1.先安装TexturePacker 2.菜单->文件->安装命令行工具").place(x=poxX, y=0)
tk.Label(window,text = "如有任何问题，请联系fuchuanjian@bytedance.com").place(x=poxX, y=20)
# 生成精灵
tk.Button(window,text = "生成精灵", command = onClickCreate, fg='green',font=('Arial', 20)).place(x=170, y=220)





window.mainloop()





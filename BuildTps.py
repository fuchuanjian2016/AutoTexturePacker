# coding=utf-8
# !/usr/bin/python

import os, shutil, json
import sys
import re
import hashlib
import collections
reload(sys)
sys.setdefaultencoding('utf8')

class BuildTps:
    def __init__(self):
        self.dir = os.path.split(os.path.realpath(__file__))[0]
        self.sourcePath = sys.argv[1]
        self.resPath = sys.argv[2]
        self.resFileName = os.path.split(os.path.split(self.resPath)[0])[1]
        self.tempPath = self.dir+"/tmp/"
        self.folderList = []
    def build(self):
        if os.path.exists(self.tempPath):
            shutil.rmtree(self.tempPath)

        self.generateFileList()
        for index,folder in enumerate(self.folderList):
            self.buildFolderTps(folder, index+1)

        if os.path.exists(self.tempPath):
            shutil.rmtree(self.tempPath)

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
        folderNameArr = folderPath.split('/')
        folderName = folderNameArr[len(folderNameArr)-1]

        

        folderRelativePath = folderPath[len(self.sourcePath):]
        resRelativePath = self.resFileName+"/" + folderRelativePath

        targetBasePath = self.tempPath + "project"+str(index)+"/"
        targetFolderPath = targetBasePath + "/folder/" + folderRelativePath

        print "buildTps "+ resRelativePath
        self.dir_copyFolder(folderPath, targetFolderPath)


        #替换模板
        tpsHandle = open("template.tps")
        tpsContent = tpsHandle.read()
        tpsHandle.close()

        tpsContent = tpsContent.replace('{textureFileName}', folderName + ".png")
        tpsContent = tpsContent.replace('{dataFileName}', folderName + ".plist")
        tpsContent = tpsContent.replace('{filename}',"folder")
        open(targetBasePath + folderName + ".tps", "w").write(tpsContent)


        #shutil.copy(folderPath, self.resPath + )
        commondStr = 'texturePacker ' + targetBasePath + folderName + ".tps"

        os.system(commondStr)
        plistHandle = open(targetBasePath + folderName + ".plist")
        plistContent = plistHandle.read()
        plistHandle.close()

        targetResFolderPath = self.resPath + folderRelativePath + "/"


        if not os.path.exists(targetResFolderPath):
            os.makedirs(targetResFolderPath)

        plistContent = re.sub('\$TexturePacker:.*\$', 'lede', plistContent)
        open(targetResFolderPath +  folderName + ".plist", "w").write(plistContent)

       
        shutil.copy(targetBasePath + folderName + ".png", targetResFolderPath + folderName + ".png")
        if os.path.exists(self.tempPath):
            shutil.rmtree(self.tempPath)

    def run(self):
        os.chdir(self.dir)
        self.build()

buildTps = BuildTps()
buildTps.run()
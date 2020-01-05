#/usr/bin/python3
import sys
import os
from XMLParser import XMLParser

class XMLDirectoryMapper ():
    def __init__ (self):
        if len(sys.argv) < 3:
            self.requestStartDir()
        else:
            self.confirmStartDir()

        self.XMLParser = XMLParser("./xml-map")

    def requestStartDir (self, startDir = ""):
        while not os.path.isdir(startDir):
            startDir = input("Please input the Directory to map: ")
        
        self.startDir = os.path.abspath(startDir)
    
    def confirmStartDir (self):
        startDir = sys.argv[2]
        self.requestStartDir(startDir)
    
    def scanDir (self, directory, xmlParent = None):
        if not xmlParent:
            xmlParent = self.originFolder

        directoryContent = os.listdir(directory)
        directoriesToRemove = []

        for content in directoryContent:

            contentPath = os.path.join(directory, content)

            if os.path.isdir(contentPath):
                folder = self.XMLParser.createElement("folder", parent = xmlParent, attributes = {"name": content})
                directoriesToRemove.append(content)

                self.scanDir(contentPath, xmlParent=folder)

        for content in directoryContent:

            contentPath = os.path.join(directory, content)

            if os.path.isfile(contentPath):
                fileSize = os.path.getsize(contentPath)

                for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
                    if fileSize < 1024.0:
                        fileSize = "%3.1f %s" % (fileSize, x)
                        break

                    if type(fileSize) != "<class 'str'>":
                        fileSize /= 1024.0

                attrs = {
                    "name": content,
                    "size": fileSize
                }

                file = self.XMLParser.createElement("file", parent = xmlParent, attributes = attrs)

    def end (self):
        self.XMLParser.save()
    
    def run (self):
        # try:
        #     self.XMLParser.open()
        # except Exception as e:
        #     self.XMLParser.create()
        
        self.XMLParser.create(rootElement="folder")

        self.XMLParser.rootElement.setAttribute("path", self.startDir)
        self.originFolder = self.XMLParser.rootElement

        self.scanDir(self.startDir)

        self.end()

if __name__ == "__main__":
    mapper = XMLDirectoryMapper()
    mapper.run()
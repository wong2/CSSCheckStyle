#/usr/bin/python
#encoding=utf-8

import sys
import os
from cssparser.CssFileParser import CssParser
from ckstyle.cmdconsole.ConsoleClass import console
from CssCheckerWrapper import CssChecker
import command.args as args

defaultConfig = args.CommandArgs()

def doCompress(fileContent, fileName = '', config = defaultConfig):
    '''封装一下'''
    parser = CssParser(fileContent, fileName)
    parser.doParse(config)

    checker = CssChecker(parser, config)

    checker.loadPlugins(os.path.realpath(os.path.join(__file__, '../plugins')))
    message = checker.doCompress()

    return checker, message

def compressFile(filePath, config = defaultConfig):
    extension = config.compressConfig.extension
    if filePath.endswith(extension):
        return
    fileContent = open(filePath).read()
    console.show('[compress] compressing %s' % filePath)
    checker, message = doCompress(fileContent, filePath, config)

    path = os.path.realpath(filePath.split('.css')[0] + extension)
    if config.printFlag:
        if os.path.exists(path):
            os.remove(path)
        console.show(message)
    else:
        open(path, 'w').write(message)
        console.show('[compress] compressed ==> %s' % path)

def compressDir(directory, config = defaultConfig):
    if config.recursive:
        compressDirRecursively(directory, config)
    else:
        compressDirSubFiles(directory, config)

def compressDirSubFiles(directory, config = defaultConfig):
    for filename in os.listdir(directory):
        if not filename.endswith('.css') or filename.startswith('_'):
            continue
        compressFile(os.path.join(directory, filename), config)

def compressDirRecursively(directory, config = defaultConfig):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if not filename.endswith('.css') or filename.startswith('_'):
                continue
            compressFile(os.path.join(dirpath, filename), config)

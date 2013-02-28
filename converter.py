#!/usr/bin/python
# -*- coding: utf-8 -*
#Author: Bruce Xin bruce.xin@gmail.com
#CreateDate: 2013-02-26 08:56
'''converter.py
convert documents to another type
'''

#stand library import
import sys
import os
from os import path
import codecs
import shutil

#third party library import
import chardet
import tifffile

_MAX_DETECT_SIZE = 100*1024
_SUPPORTED_FILE_TYPE = set(['.doc', '.xls', '.docx', '.xlsx', '.txt', '.tif', '.tiff'])

def re_encoding_txt(fileName, newFileName):
    buf = open(fileName, 'rb').read(_MAX_DETECT_SIZE)
    result = chardet.detect(buf)
    if result['confidence'] >= 0.5:
        abuf = unicode(open(fileName, 'rb').read(), result['encoding'])
        codecs.open(newFileName, 'wb', 'utf8').write(abuf)
        return newFileName
    else:
        return fileName


def _convert_tiff(filePath, newFileName, newFilePath):
    baseName, _ = path.splitext(newFileName)
    tmpPDF = path.join('/tmp', baseName, '.pdf')
    os.system('unoconv -f pdf -o %s %s'%(tmpPDF, filePath))
    tmpTIF = path.join('/tmp', newFileName)
    os.system('gs -q -sDEVICE=tiffg3 -r204x98 -dBATCH -dPDFFitPage -dNOPAUSE -sOutputFile=%s %s'%(tmpTIF, tmpPDF))
    tf = tifffile.TiffFile(tmpTIF)
    tmpPath = _rename_tiff_for_page(tmpTIF)
    shutil.move(tmpPath, newFilePath)
    return outPath


def _rename_tiff_for_page(filePath):
    baseName, _ = path.splitext(filePath)
    tf = tifffile.TiffFile(filePath)
    pageNum = len(tf.pages)
    outPath = path.join('%s_%d.tif'%(baseName, pageNum))
    shutil.move(filePath, outPath)
    return outPath


def _convert_tiff_name(filePath, newFileName, newFilePath):
    basePath, fileName = path.split(filePath)
    tmpPath = path.join('/tmp', newFileName)
    shutil.move(filePath, tmpPath)
    outPath = _rename_tiff_for_page(tmpPath)
    shutil.move(outPath, newFilePath))
    outBasePath, outFileName = path.split(outPath)
    return path.join(newFilePath, outFileName)


def convert_tiff(filePath, newFileName, newFilePath):
    _, extName = path.splitext(filePath)
    if extName not in _SUPPORTED_FILE_TYPE:
        raise NotImplemented(extName)

    if extName == '.txt':
        _, fileName = path.split(filePath)
        aFilePath = re_encoding_txt(filePath, path.join('/tmp', fileName))
    elif extName == '.tif' or extName == '.tiff':
        return _convert_tiff_name(filePath, newFileName, newFilePath)
    else:
        aFilePath = filePath

    return _convert_tiff(aFilePath, newFileName, newFilePath)


if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Usage: converter <infile> [outPath]"
        exit(0)

    inPath = sys.argv[1]
    if len(sys.argv) == 3:
        outPath = sys.argv[2]
    else:
        outPath = '.'

    _, fileName = path.split(inPath)
    baseName, extName = path.splitext(fileName)

    newPath = convert_tiff(inPath, baseName+".tif", outPath)
    print "convert success, new tif file is ", newPath




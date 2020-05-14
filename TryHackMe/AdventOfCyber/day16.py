# Day File Confusion, create by gu2rks
import sys
import os
import zipfile
import exiftool

def task1(): 
    """ 
    How many files did you extract(excluding all the .zip files)
    """
    # get all files
    files = os.listdir('./final-final-compressed')
    for file in files:
        # now unzip it
        with zipfile.ZipFile('./final-final-compressed/'+file, 'r') as zip_ref:
            zip_ref.extractall('./extracted')
    # get all files agains
    extracted = os.listdir('./extracted')
    print('Extracted %s files' % len(extracted))

def task2():
    """ 
    How many files contain Version: 1.1 in their metadata?
    Note: move this scrip inside ./extracted
    lookingfor = {'SourceFile': '4jGg.txt', 'ExifTool:ExifToolVersion': 11.94, 'File:FileName': '4jGg.txt',
    'File:Directory': '.', 'File:FileSize': 2844, 'File:FileModifyDate': '2020:05:13 22:02:50-04:00', 
    'File:FileAccessDate': '2020:05:13 22:39:53-04:00', 'File:FileInodeChangeDate': '2020:05:13 22:02:50-04:00', 
    'File:FilePermissions': 644, 'File:FileType': 'MIE', 'File:FileTypeExtension': 'MIE', 'File:MIMEType': 'application/x-mie', 
    'XMP:XMPToolkit': 'Image::ExifTool 10.80', 'XMP:Version': 1.1}
    """
    count = 0
    files = os.listdir('./') # get all files
    
    with exiftool.ExifTool() as et: # get exiftool
        files_metadata = et.get_metadata_batch(files) # get all files metadata
    for metadata in files_metadata: # get file metadata one by one
        if 'XMP:Version' in metadata: # check if metadata contains 'XMP:Version'
            count = count + 1 # if so -> count it
    
    print('Total Version:1.1 files : %s' %count) 

def task3():
    """
    Which file contains the password?
    Note: move this scrip inside ./extracted
    password is 'scriptingpass'
    """
    files = os.listdir('./') # get all files
    for file in files: # get file name one by one
        with open(file, 'r', encoding = "ISO-8859-1") as reader: # open it
            data = reader.read() # read it
        if 'password' in data: # check if it contain password
            print(file) # if so -> print out file name

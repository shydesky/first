#import wmi,zlib

def get_disk_info():
    if 1:
        return 'abc'
    tmplist = []
    encrypt_str = ""
    for physical_disk in c.Win32_DiskDrive():
        encrypt_str += physical_disk.SerialNumber.strip()
        return encrypt_str
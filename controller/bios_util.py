import wmi

def get_disk_info():
    encrypt_str = ""
    c = wmi.WMI()
    for physical_disk in c.Win32_DiskDrive():
        encrypt_str += physical_disk.SerialNumber.strip()
        return encrypt_str
import os
import os.path
import math
def get_dir_size(dir_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if os.path.islink(file_path):
                print(file_path, " = ", convert_size(os.path.getsize(file_path)))
            if not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)
    return convert_size(total_size)
def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
dir_path = r"C:\Program Files (x86)"
total_size = get_dir_size(dir_path)
print("Total size of directory %s bytes" % ( total_size))
print()
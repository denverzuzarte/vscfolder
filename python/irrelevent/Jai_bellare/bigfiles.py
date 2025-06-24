from pathlib import Path
from subprocess import run

def sizeof_fmt(num):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:7.1f}{unit}B"
        num /= 1024.0
    return f"{num:7.1f}YiB"

files = []
for path in Path('.').glob('**/*'):
    if not path.is_file():
        continue
    pair = (path, path.stat().st_size)

    files.append(pair)
    files.sort(key=lambda x: x[1], reverse=True)

    del files[20:]  # max 20 files

    run(['cls'])
    for file, size in files:
        print(sizeof_fmt(size), ':', file)
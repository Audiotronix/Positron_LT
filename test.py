import glob, os
PATH = r'/Users/simon/Desktop/dev/Positron_LT/Parts'


files = glob.glob(PATH+'/**/*.stl', recursive=True)
files += glob.glob(PATH+'/**/*.step', recursive=True)
for file in files:
    os.remove(file)
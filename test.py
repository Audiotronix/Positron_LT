import glob, os
PATH = r''


files = glob.glob(PATH+'/**/*.stl', recursive=True)
files += glob.glob(PATH+'/**/*.step', recursive=True)
for file in files:
    os.remove(file)
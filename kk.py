from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("./data") if isfile(join("./data", f))]

for i in onlyfiles:
    if not i.__contains__(".csv"):
        onlyfiles.remove(i)
print(onlyfiles)
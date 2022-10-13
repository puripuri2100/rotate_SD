import sys

input_str = sys.argv[1]


f = open('tmp1.txt', 'a', encoding='UTF-8')

for s in input_str.split('\n'):
    ms = "\n    " + "{"+"\"tag\":"+f"\"{s}\""+"},"
    f.write(ms)



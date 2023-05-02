import re

def re_extract(file:str, output):
    """通过正则匹配的方式从文件提取内容, 然后按行打印出来
    用途: xls, pdf文件中复制学号, 姓名等信息, 提取生成字典
    """
    with open(file, 'r', encoding='utf-8') as f, \
        open(output,'w', encoding='utf-8') as outfile:
        content = f.read()

        pattern = re.compile('[a-z]{3,}')
        matches = pattern.findall(content)

        for match in matches:
            outfile.write(f"{match}\n")
            # print(match)

def deduplication(file, *args):
    """ 对文件内容进行去重, 整理字典时可以用 
    直接对原文件去重覆盖, 如果不放心可以备份
    """
    with open(file, 'r', encoding='utf-8') as f:
        lineset = set()
        line = f.readline()
        while line:
            lineset.add(line.strip())
            line = f.readline()

    with open(file, 'w', encoding='utf-8') as f:
        for i in lineset:
            f.write(i+'\n')
            # print(i)

if __name__ == '__main__':
    # re_extract("example.txt","output.txt")
    deduplication("./1.txt")
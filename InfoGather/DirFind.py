"""
Filename: DirFind.py
Author: Vin0sen
Contact: 464029561@qq.com
"""
import sys, os, time
import threading
import argparse
import random
import numpy
import requests

class DirFind():
    """
        目录扫描
    """
    def __init__(self) -> None:
        self.position = os.path.dirname(__file__)
        self.wordlist = self.position + '/db/dict.txt'
        self.user_agent = self.position + '/db/ua.txt'
        self.out_file = self.position + '/db/output_'+ \
            time.strftime('%Y-%m-%d',time.localtime(time.time())) + \
            '.txt'
        # self.urlsfile = self.position + '/db/urls.txt'
        
        self.param_parse()

    def param_parse(self):
        """对命令行参数进行解析"""
        # create a parser
        parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' +
                                         sys.argv[0] + " -u https://www.baidu.com/")
        # append params
        parser.add_argument("-u", "--url")
        parser.add_argument("-f", "--file")  # , default=self.urlsfile
        parser.add_argument("-t", "--threads", type=int, default=2)
        parser.add_argument("-o", "--output", default=self.out_file)
        # parse params
        self.args = parser.parse_args()

    def run(self):
        """启动函数"""
        if self.args.url == None and self.args.file == None:
            print("-u URL or -f FILE is required")
            sys.exit()
        
        wordlist = numpy.loadtxt(self.wordlist, encoding='utf-8', dtype="str")
        self.assign_thread(wordlist, len(wordlist), self.args.threads)

    def assign_thread(self, wordlist, length, sum_threads):
        """ 分配线程. 参数分别为 字典对象; 字典长度; 总线程数 """
        num_per_thread = length // sum_threads  # 计算每个线程处理的量
        
        for i in range(sum_threads):
            start = i * num_per_thread
            end = start + num_per_thread

            # 每个线程需要处理的列表
            list_for_thread = wordlist[start:end]

            # 创建和启动线程
            thread = threading.Thread(target=self.process, args=(list_for_thread,))
            thread.start()

        # 处理最后一组网址
        list_for_thread = wordlist[sum_threads * num_per_thread:]
        thread = threading.Thread(target=self.process, args=(list_for_thread,))
        thread.start()

    def process(self, process_list):
        """
        发起请求, 处理响应结果
        """
        # 若指定 -u , 
        if self.args.url:
            self.sendrequest(self.args.url, process_list)
        # 未指定 -u , 采用 -f , 批量进行请求, 默认读取 db/urls.txt
        else:
            with open(self.args.file, 'r', encoding="utf-8") as file:
                url = file.readline().strip()
                while url:
                    self.sendrequest(url, process_list)
                    url = file.readline()
        
    def sendrequest(self, host, process_list):
        for uri in process_list:
            url = f"{host}" + uri.strip()

            headers = {
                'User-Agent': self.random_agent(),
                'Referer': 'https://www.bing.com/',
            }
            try:
                response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
            except:
                print('An Unknow Error Happened')
                continue

            code = response.status_code

            # 对响应结果 以不同颜色打印
            if os.name == "nt":  # 针对于 windows 系统的处理
                os.system("")
            if code == 200:
                print(f'\033[1;32m{code}: {url}\033[0m')
            elif code == 302:
                redirected_url = response.headers['Location']
                print(f'\033[1;33m{code}: {url} --> {redirected_url}\033[0m', )
            else:
                print(f'{code}:', url)

    def random_agent(self):
        """ 设置随机的User-Agent """
        with open(self.user_agent, 'r', encoding="utf-8") as file:
            random_row = random.randint(1, 15)
            line = file.readline()
            count = 1
            while line:
                if count >= random_row:
                    break
                line=file.readline()
                count += 1
        return line.strip()


if __name__ == '__main__':
    Obj = DirFind()
    Obj.run()

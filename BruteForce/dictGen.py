import itertools

month = ['01','02','03','04','05','06','07','08','09','10','11','12']

def sfz_last6(sex):
    """ 身份证后六位字典生成; 总计 34万 + ,即便知道性别, 也要爆破17万多次 """
    days = month + ['13','14','15','16','17','18','19',
                    '20','21','22','23','24','25',
                    '26','27','28','29','30','31']
    if sex == 1:  # 男
        sexflag = '13579'  
    elif sex == 0:  # 女
        sexflag = '24680'
        
    with open(f"./身份证后6位-{sex}.txt", 'w') as file:
        for index in range(31):
            day = days[index]
            check = '0123456789X'
            other = '0123456789'
            nums = (itertools.product(other, other, sexflag, check))
            for num in nums:
                file.write(day +"".join(num)+'\n')

if __name__ == '__main__':
    sfz_last6()

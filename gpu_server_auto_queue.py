import os
import time

import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = ''  # 发件人邮箱账号
my_pass = '' # 邮箱密码 参考 https://www.runoob.com/python/python-email.html 中 “使用第三方 SMTP 服务发送” 的方法
my_user = '' # 收件人邮箱账号
sub_text = "IDLE GPU, CHECK TASK in hf3090"
GPU_NUM = 8
CMD_list = ['python main_mem_my_with_dist.py --cfg cfg/coco_memory_top10.yml']

# CMD_list = [' python 1.py &', ' python 2.py &']
for i, ele in enumerate(CMD_list):
    CMD_list[i] = ' ' + ele + ' &'

def mail(text):
    ret = True
    try:
        msg = MIMEText('IDLE GPU', 'plain', 'utf-8')
        msg['From'] = formataddr(["From Local server", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = text # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

def gpu_info():
    gpu_status = os.popen('nvidia-smi | grep %').read().split('|')
    gpu_memory = []
    gpu_power = []
    for i in range(GPU_NUM):
        gpu_memory.append(int(gpu_status[2 + 4 * i].split('/')[0].split('M')[0].strip()))
        gpu_power.append(int(gpu_status[1 + 4 * i].split('   ')[-1].split('/')[0].split('W')[0].strip()))
    return gpu_power, gpu_memory


def narrow_setup():
    gpu_power, gpu_memory = gpu_info()
    pointer = 0
    while pointer < len(CMD_list):
        while min(gpu_memory) > 1000 or min(gpu_power) > 50:  # set waiting condition
            time.sleep(30)
            gpu_power, gpu_memory = gpu_info()
        text = sub_text + '-' + str(np.argmin(np.array(gpu_memory)))
        mail(text)
        print('CUDA_VISIBLE_DEVICES={}'.format(str(np.argmin(np.array(gpu_memory))) + CMD_list[pointer]))
        os.system('CUDA_VISIBLE_DEVICES={}'.format(str(np.argmin(np.array(gpu_memory))) + CMD_list[pointer]))
        time.sleep(300)
        pointer += 1
        gpu_power, gpu_memory = gpu_info()


if __name__ == '__main__':
    narrow_setup()

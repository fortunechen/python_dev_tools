import os
import sys
import time

import numpy as np

GPU_NUM = 8
CMD = ' python 1.py'


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
    while min(gpu_memory) > 1000 or min(gpu_power) > 20:  # set waiting condition
        gpu_power, gpu_memory = gpu_info()
        time.sleep(30)
    print('\n' + CMD)
    print(np.argmin(np.array(gpu_memory)))
    os.system('CUDA_VISIBLE_DEVICES={}'.format(str(np.argmin(np.array(gpu_memory))) + CMD))

if __name__ == '__main__':
    narrow_setup()
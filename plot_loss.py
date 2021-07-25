import argparse

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--log_file', type=str, help='path to loss log file')

args = parser.parse_args()
log_file = args.log_file

loss_list = []
with open(log_file, 'r') as f:
    for line in f.readlines():
        if 'train_loss' in line:
            loss_list.append(float(str(line.split('=')[1][1:6])))

plt.plot(list(range(len(loss_list))), loss_list)
plt.savefig('loss.jpg')

print("done")
from tokenize import group
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys 

DELTA_T = 0.05

data = pd.read_csv('./data/' + sys.argv[1] + '-h-vs-t.csv')
data['delta_y'] = 1 - data['height']

#calculate velocities using derivative approximation
velocity = [None for i in range(0, data.shape[0])]
print(data.shape[0])
for i in data.index: 
	before = max(0, i - 1)
	after = min(data.shape[0] - 1, i + 1)
	dt = DELTA_T * (1 if (i == 0 or i == data.shape[0] - 1) else 2)
	
	velocity[i] = ((data['delta_y'][after] - data['delta_y'][before])/dt)

print(velocity)

#approximate the acceleration as a function of time
acceleration = [None for i in range(0, data.shape[0])]
for i in data.index: 
	before = max(0, i - 1)
	after = min(data.shape[0] - 1, i + 1)
	dt = DELTA_T * (1 if (i == 0 or i == data.shape[0] - 1) else 2)
	
	acceleration[i] = ((velocity[after] - velocity[before])/dt)

print(acceleration)

data['acceleration'] = acceleration
data['velocity'] = velocity

data.to_csv('./output/' + sys.argv[1] + '-h-vs-t-out.csv')

for index, subdata in enumerate([data.iloc[:8], data.iloc[8:]]):
	d_title = ('pre' if index == 0 else 'post')
	sns.lmplot(data=subdata, x='time', y='delta_y', order = 2)
	ax = plt.gca()
	ax.set_title('y-displacement vs. time - ' + d_title + '-collision')

	sns.lmplot(data=subdata, x='time', y='velocity', order = 1)
	ax = plt.gca()
	ax.set_title('velocity vs. time - ' + d_title + '-collision')

	sns.relplot(data=subdata, x='time', y='acceleration')
	ax = plt.gca()
	ax.set_title('acceleration vs. time - ' + d_title + '-collision')

plt.show()

#Drag is negligible, as it is shown within experimental error that the acceleration remains constant


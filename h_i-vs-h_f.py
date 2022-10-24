from tokenize import group
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

heights = pd.read_csv('./data/heights.csv')

print(heights.index)

heights['mean h_f'] = (heights['t1'] + heights['t2'] + heights['t3'] + heights['t4'])/4

h_i = []
h_f = []
ball = []
for row in heights.index: 
	for col in ['t1', 't2', 't3', 't4']:
		ball.append(heights.loc[row, 'ball'])
		h_i.append(heights.loc[row, 'h_i'])
		h_f.append(heights.loc[row, col])

parsed_heights = pd.DataFrame({'h_i': h_i, 'h_f': h_f, 'ball': ball})
parsed_heights['COR'] = np.sqrt(parsed_heights['h_f']/parsed_heights['h_i'])
print(parsed_heights)

grouped_by_ball = parsed_heights.groupby(by='ball')

for ball in ['rubber', 'golf']:
	data_for_ball = grouped_by_ball.get_group(ball)
	data_for_ball.to_csv('./output/' + ball + '-COR')
	print(data_for_ball)
	print('Mean COR: ', data_for_ball['COR'].mean(), '\n')
	sns.lmplot(data=data_for_ball, x='h_i', y='h_f', order = 1)
	ax = plt.gca()
	ax.set_title('h_f vs. h_i for ' + ball + ' ball')

plt.show()
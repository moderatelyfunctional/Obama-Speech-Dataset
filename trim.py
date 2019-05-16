import random

train_data = []
val_data = []
with open('data.txt', 'r') as data:
	for line in data:
		if random.random() < 0.1:
			val_data.append(line)
		else:
			train_data.append(line)

with open('train_split.txt', 'w') as train_txt:
	for line in train_data:
		line = line.strip()
		if line[-1] != '.':
			if not (line[-1] == '-' or line[-1] == ','):
				line += '.'
		train_txt.write('/home/modfun/Desktop/Obamatron/{}\n'.format(line))

with open('val_split.txt', 'w') as val_txt:
	for line in val_data:
# To test python generators to optimize batch access.
from csv import DictReader

path = '../../../../DATA/kaggle-avazu-ctr-prediction/'
train = path + 'train'

def fn_batchgenerator(path,start_row=0,batch_size=5,nmax=20):
	# Init the output list.
	output = []
	# Open the file using the csv dictreader and iterate over each row
	for ix, row in enumerate(DictReader(open(path))):
		# If the row is after the start-row
		if (ix+1) >= start_row:
			# Append the row to the output list
			output.append((ix,row))
			# If we have a full batch, yield (return) it and reset the output.
			if (ix+2-start_row) % batch_size == 0:
				yield output
				output = []
			# If we have hit our max number of rows, break out.
			if (ix+1-start_row) == nmax:
				break


# For each batch that is returned from the file
for batch in fn_batchgenerator(path=train,start_row=3,batch_size=3,nmax=15):
	print batch, '\n\n'

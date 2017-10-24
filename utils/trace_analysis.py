import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

trace = '/home/msiquier/IOSTACK/ArcturTrace/to_execute_arctur_equispaced.csv'
trace2 = '/home/msiquier/IOSTACK/ArcturTrace/arctur_trace_final.csv'

with open(trace, 'rb') as csvfile:
	data = csv.reader(csvfile, delimiter=',')
	date = []
	objs = []
	size = []
	for row in data:
		#for trace:
		date.append(datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f'))
		#for trace2:
		#date.append(datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'))
		size.append(float(row[4])/(1024*1024))
		objs.append(row[3])

print "Total rows in trace: " + str(len(objs))
print "Different objects: " + str(len(set(objs)))
print "Mean size of all objects: " + str(np.mean(size)) 
print "Max size of all objects: " + str(np.max(size))

diffs = [(j-i).total_seconds() for i, j in zip(date[:-1], date[1:])]

plt.hist(diffs, bins=100)
plt.title('Time differences')
plt.show()

plt.plot(diffs)
plt.title('Time differences')
plt.show()

plt.boxplot(diffs)
plt.title('Time differences')
plt.show()

#plt.hist(size, bins='auto')
#plt.title('Size')
#plt.show()

plt.plot(size)
plt.title('Size')
plt.show()

plt.boxplot(size)
plt.title('Size')
plt.show()
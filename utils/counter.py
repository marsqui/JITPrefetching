import csv
import argparse
import itertools
import numpy as np
import random
import math
from matplotlib import pyplot as plt
from datetime import datetime
from collections import defaultdict, Counter


def main(results_file, number, prefe, plot):

	#input_file = open(results_file)
	input_file = results_file

	csv_reader = csv.reader(results_file, delimiter='\t')

	objs_throughput = []
	objs_download_time = []
	objs_prefetched = []
	i = 0

	for row in csv_reader:
		if prefe:
			if float(row[3]) < 10:
				objs_download_time.append(float(row[3]))
				objs_throughput.append(float(row[4]))
				if prefe:
					objs_prefetched.append(row[12])
			else:
				i+=1

	if number:
		statistics(objs_download_time[:number], 'Download time', plot)
		statistics(objs_throughput[:number], 'Throughput', plot)
		if prefe:
			prefetched = [pref for pref in objs_prefetched[:number] if pref=='True']

	else:
		statistics(objs_download_time, 'Download time', plot)
		statistics(objs_throughput, 'Throughput', plot)
		if prefe:
			prefetched = [pref for pref in objs_prefetched if pref=='True']

		

	print "Number of objects with t>10: "+ str(i)
	if prefe:
		print "Number of prefetched objects: "+ str(len(prefetched))

def mergelog(results_file):
	input_file = results_file
	csv_reader = csv.reader(results_file, delimiter='\t')
	results = [row for row in csv_reader]
	log_file= raw_input('Enter a log file: ') 
	f = open(log_file)
	log_reader = csv.reader(f, delimiter=' ')
	log = [row for row in log_reader]
	merged_file= raw_input('Enter a merged filename: ')
	myfile = open(merged_file, 'wb')
	wr = csv.writer(myfile, delimiter='\t')

	for row in results[:number]:
		found = False
		for row2 in log:
			if row[11] == row2[7]:
				time = datetime.strptime(row[0], '%H:%M:%S')
				time2 = datetime.strptime(row2[2], '%H:%M:%S')
				diff = time - time2
				if abs(diff.total_seconds()) < 15:
					row.append(True)
					found = True
					break
		if not found:
			row.append(False)
		wr.writerow(row)


def statistics(data, title, plot=False):
	print str(title) + ' Number of rows: '+ str(len(data))
	print 'Max ' + title + ': '+ str(max(data)) 
	print 'Min ' + title + ': '+ str(min(data))
	print 'Avg ' + title + ': '+ str(sum(data) / len(data))

	if plot:
		plt.xlim(0,3)
		plt.hist(data, 500, facecolor='green')
		plt.title(title)
		plt.xlabel('time (500 evenly spaced bins)')
		plt.ylabel('count')

		plt.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Process a SwiftWorkloadGenerator results file')

	parser.add_argument('File', metavar='results_file', type=open,
                    help='Results file')

	parser.add_argument('-n', dest='number', type=int,
                        help='Number of rows to read', default=False)

	parser.add_argument('-p', dest='plot', action='store_const',
                    const=True, default=False,
                    help='Plot some histograms')

	parser.add_argument('--prefetch', dest='prefetch', action='store_const',
                    const=True, default=False,
                    help='The results file includes prefetch stats')

	parser.add_argument('--mergelog', dest='merge', action='store_const',
                    const=True, default=False,
                    help='Merge results file with log file')

	args = parser.parse_args()
	if args.merge:
		mergelog(args.File)
	else:
		main(args.File, args.number, args.prefetch, args.plot)
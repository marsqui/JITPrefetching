import csv
import numpy as np
import argparse
import matplotlib.pyplot as plt



def main(file_noprefetch, file_prefetch, number):
	noprefetch = csv.reader(file_noprefetch, delimiter='\t')
	prefetch = csv.reader(file_prefetch, delimiter='\t')
 	sizes = []
	total_no = 0
	total_pref = 0
	time_differences = []
	for rown, row in zip(noprefetch, prefetch)[:number]:
		total_no = total_no + float(rown[3])
		total_pref = total_pref + float(row[3])
		sizes.append(float(rown[4]))
		time_differences.append( (float(rown[3]) - float(row[3])) )

	print "Total download time with no prefetch: "+ str(total_no)
	print "Total download time with prefetch: "+ str(total_pref)
	plots(time_differences, 'Download Time Differences', number, True, True, True, True)

def plots(data, title='', number=1, normal=True, boxplot=True, histo=True, ecdf=False):
	if normal:
		plt.scatter(np.arange(0,len(data),1), data)
		plt.title(title)
		plt.show()

	if boxplot:
		plt.boxplot(data)
		plt.title(title)
		plt.show()
		plt.savefig('foo.png')

	if histo:
		plt.hist(data, bins=100)
		plt.title(title)
		plt.show()
		#plt.savefig('foo.png')

	if ecdf:
		plt.hist(data, bins=100, cumulative=True)
		plt.title(title)
		plt.yticks(np.arange(0, number, number/10))
		plt.gca().set_yticklabels(np.arange(0, 1.1, 0.1))
		plt.savefig('foo.png')
		plt.show()
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Prefetch Results Comparison')

	parser.add_argument('File_noprefetch', metavar='results_noprefetch', type=open,
                    help='Results without prefetch file')

	parser.add_argument('File_prefetch', metavar='results_prefetch', type=open,
                    help='Results with prefetch file')

	parser.add_argument('-n', dest='number', type=int,
                        help='Number of rows to read', default=False)
	

	args = parser.parse_args()
	main(args.File_noprefetch, args.File_prefetch, args.number)



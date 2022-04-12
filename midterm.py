import collections
import itertools
from itertools import chain
import csv
import time
import copy


# read in the given .csv database file 'filename' and
# return the values in a 2D array 'rows'
def readfile(filename):
	file = open(filename)
	type(file)
	csvreader = csv.reader(file)
	rows = []

	for row in csvreader:
		rows.append(row)

	file.close()

	# remove transaction id and sort in alphabetical order
	for row in rows:
		row.pop(0)

	return rows


# takes as input a candidate_list of potentially frquent transactions,
# the databse of transactions (trans_list), and the minimum support
# specified by the user.  returns the dictionary of frequent values
# found in the database
def count_freq(candidate_list, trans_list, min_sup):
	freq_dict = {}
	count = 0

	for cand in candidate_list:
		for trans in trans_list:
			if set(cand).issubset(set(trans)):
			#if all(items in trans for items in cand):
				count += 1
		freq_dict.update({cand: count})
		count = 0

	final_dict = {key:val for key, val in freq_dict.items() if val >= min_sup}
	return final_dict

# returns the support of the given transaction in the db
def find_support(sup_x, num_trans):
	return sup_x / float(num_trans)

# takes as input a database of transactions, a minimun support value,
# and a minimum confidence vale.  returns the association rules
# derived from the given database that meet the minimum support and 
# confidence
def apriori(db, support, confidence):
	data = readfile(db)
	num_trans = len(data)
	min_sup = num_trans * support
	k = 2

	flat = list(chain.from_iterable(data))
	count = collections.Counter(flat)
	# find frequent 1-itemsets
	freq_one_dict = {key: val for key, val in count.items() if val >= min_sup}

	L = freq_one_dict.keys()
	all_freq_trans = []
	all_freq_dict = {}

	# get frequent itemsets until the list of frequent items sets becomes
	# empty meaning there will be no more frequent items
	while L:
		candidate = list(itertools.combinations(freq_one_dict, k))
		L = count_freq(candidate, data, min_sup)
		for key, val in L.items():
			all_freq_dict.update({key: val})
		all_freq_trans.append(L.keys())
		k += 1

	loop_dict = all_freq_dict.copy()
	all_freq_dict.update(freq_one_dict)

	#print all_freq_dict

	tmp = 0
	# calculate values and print out the corresponding rules
	for key, val in loop_dict.items():
		cnt = 0

		perms = list(itertools.permutations(key))
		if len(perms) == 6:
			perms[2], perms[3] = perms[3], perms[2]
		sup = find_support(all_freq_dict.get(perms[tmp]), num_trans)

		x = {}
		for perm in perms:
			x.update({perm: val})
		all_freq_dict.update(x)
		
		for perm in perms:
			iterate = len(perm)
			left = iterate - 1
			right = iterate - left

			lset = perm[0: left]
			rset = perm[left: left+1]

			num = all_freq_dict.get(lset)
			if len(lset) == 1:
				num = all_freq_dict.get(''.join(lset))

			if len(perm) > 2:
				if cnt > 2:
					num = freq_one_dict.get(''.join(rset))
					conf = sup / find_support(num, num_trans)
					if conf > confidence:
						print('[' + str(rset) + ' ---> ' + str(lset) + ' (' + str(sup) + ', ' + str(conf) + ')]')
					cnt += 1
					continue


			conf = sup / find_support(num, num_trans)
			if conf > confidence:
				print('[' + str(lset) + ' ---> ' + str(rset) + ' (' + str(sup) + ', ' + str(conf) + ')]')

			cnt += 1



# tenumerates all possible combonations of the items in the databse
# and returns the same associations rules that the apriori method does
def brute_force(all_items, db, support, confidence): 
	data = readfile(db) # read in database file and remove trans id
	num_trans = len(data)
	min_sup = num_trans * support
	items = readfile(all_items)
	k = 2
	flat_items = []
	# flatten item list
	for item in items:
		flat_items.append(item[0])

	freq_dict = {}
	count = 0
	for it in flat_items:
		for trans in data:
			for obj in trans:
				if obj == it:
					count += 1
		freq_dict.update({it: count})
		count = 0
	
	freq_one_dict = {key: val for key, val in freq_dict.items() if val >= min_sup}

	all_freq_trans = []
	tmp_dict = {}
	final_dict = {}
	L = flat_items
	
	while(k < 5):
		candidate = list(itertools.combinations(freq_dict.keys(), k))
		L = count_freq(candidate, data, min_sup)
		for key, val in L.items():
			final_dict.update({key: val})
		all_freq_trans.append(L.keys())
		k += 1

	loop_dict = freq_one_dict.copy()
	loop_dict.update(final_dict)

	tmp = 0
	# calculate values and print out the corresponding rules
	for key, val in final_dict.items():
		cnt = 0
		perms = list(itertools.permutations(key))
		if len(perms) == 6:
			perms[2], perms[3] = perms[3], perms[2]

		sup = find_support(loop_dict.get(perms[tmp]), num_trans)

		x = {}
		for perm in perms:
			x.update({perm: val})
		final_dict.update(x)
		
		for perm in perms:
			iterate = len(perm)
			left = iterate - 1
			right = iterate - left

			lset = perm[0: left]
			rset = perm[left: left+1]
			num = final_dict.get(lset)

			if len(lset) == 1:
				num = loop_dict.get(''.join(lset))

			if len(perm) > 2:
				if cnt > 2:
					num = loop_dict.get(''.join(rset))
					conf = sup / find_support(num, num_trans)
					if conf > confidence:
						print('[' + str(rset) + ' ---> ' + str(lset) + ' (' + str(sup) + ', ' + str(conf) + ')]')
					cnt += 1
					continue

			conf = sup / find_support(num, num_trans)
			if conf > confidence:
				print('[' + str(lset) + ' ---> ' + str(rset) + ' (' + str(sup) + ', ' + str(conf) + ')]')
			cnt += 1



print('---------APRIORI------------')
start = time.time()
apriori('midterm_db_1.csv', 0.15, 0.5)
end = time.time()
print('\nTOTAL TIME: ' + str(end - start))


print('\n\n--------BRUTE FORCE----------')
start = time.time()
brute_force('items_db.csv', 'midterm_db_1.csv', 0.15, 0.5)
end = time.time()
print('\nTOTAL TIME: ' + str(end - start) + '\n\n\n\n\n')



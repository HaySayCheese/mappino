from collections import Counter
import csv

# open files
file_with_dom_numbers = open('dom_ria_grabber/numbers.txt', 'r')
file_with_olx_numbers = open('olx_grabber/numbers.txt', 'r')
realtors_numbers_file = open('realtors_numbers.txt', 'w')
# read realtors numbers from olx.ua and dom.ria.ua than combine them into one list
dom_numbers = file_with_dom_numbers.readlines()
olx_numbers = file_with_olx_numbers.readlines()
realtors_numbers = dom_numbers + olx_numbers
# count repeats of unique realtors numbers and make dictionary like {number: count_of_repeats}
unique_realtors_numbers = Counter(realtors_numbers)
csvwriter = csv.writer(realtors_numbers_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
# if count_of_repeats > 1 write number and count to file in csv format
for number in unique_realtors_numbers:
    if unique_realtors_numbers[number] > 1:
        csvwriter.writerow([number[:-1], unique_realtors_numbers[number]])
# close files
file_with_olx_numbers.close()
file_with_dom_numbers.close()
realtors_numbers_file.close()

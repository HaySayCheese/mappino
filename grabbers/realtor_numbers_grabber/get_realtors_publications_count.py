from collections import Counter
import csv


def count_realtors_publications(*files_path):
    # there is no need to check if files_path is None because in that case it will return 0
    files = []
    # open files
    for file_path in files_path:
        files.append(open(file_path, 'r'))
    total_count = 0
    for numbers_file in files:

        realtors_numbers = numbers_file.readlines()
        # count repeats of unique realtors numbers and make dictionary like {number: count_of_repeats}
        unique_realtors_numbers = Counter(realtors_numbers)

        for number in unique_realtors_numbers:
            if unique_realtors_numbers[number] > 2:
                total_count += unique_realtors_numbers[number]
    # close files
    for numbers_file in files:
        numbers_file.close()

    return total_count

print count_realtors_publications('dom_ria_grabber/rent_lv_numbers.txt', 'dom_ria_grabber/sale_lv_numbers.txt',
                                  'dom_ria_grabber/daily_rent_lv_numbers.txt')

print count_realtors_publications('dom_ria_grabber/rent_h_numbers.txt', 'dom_ria_grabber/sale_h_numbers.txt',
                                  'dom_ria_grabber/daily_rent_h_numbers.txt')

print count_realtors_publications('olx_grabber/rent_lv_numbers.txt', 'olx_grabber/sale_lv_numbers.txt',
                                  'olx_grabber/daily_rent_lv_numbers.txt')

print count_realtors_publications('olx_grabber/rent_h_numbers.txt', 'olx_grabber/sale_h_numbers.txt',
                                  'olx_grabber/daily_rent_h_numbers.txt')

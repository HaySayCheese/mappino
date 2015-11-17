from collections import Counter


def select_realtors(path_to_file, path_to_realtors_file):
    # open files
    file_with_numbers = open(path_to_file, 'r')
    realtors_numbers_file = open(path_to_realtors_file, 'w')
    # read realtors numbers from olx.ua and dom.ria.ua than combine them into one list
    numbers = file_with_numbers.readlines()
    # count repeats of unique realtors numbers and make dictionary like {number: count_of_repeats}
    unique_realtors_numbers = Counter(numbers)
    # if count_of_repeats > 1 write number and count to file in csv format
    for number in unique_realtors_numbers:
        if unique_realtors_numbers[number] > 2:
            realtors_numbers_file.write(number)
            print number, unique_realtors_numbers[number]
    # close files
    file_with_numbers.close()
    realtors_numbers_file.close()

select_realtors('olx_grabber/daily_rent_h_numbers.txt', 'daily_rent_h_realtors_numbers.txt')
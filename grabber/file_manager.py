import phonenumbers


def add_to_file(numbers):
    # defines numbers
    phones = phonenumbers.PhoneNumberMatcher(numbers, 'UA')
    for phone in phones:
        # format number
        phone = phonenumbers.format_number(phone.number, phonenumbers.PhoneNumberFormat.E164)
        print phone
        # add number to file
        file_with_numbers = open('./numbers.txt', 'a')
        file_with_numbers.write(phone+'\n')
        file_with_numbers.close()

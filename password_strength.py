import sys
import re

def get_password_strength(password):
    strength = rate_case_sensitivity(password)
    strength += rate_special_characters(password)
    strength += rate_numeric(password) 
    strength += rate_length(password)
    strength = check_for_prohibition(password, strength)
    return strength


def check_for_prohibition(password, strength, prohibited):
    for forbidden in prohibited:
        if password.lower() == forbidden.lower():
            return 1
        elif forbidden.lower() in password.lower():
            strength +=1
        else:
            strength +=2
    return strength


def rate_case_sensitivity(password):
    last_case = password[0].isupper()
    count_switches = 0
    for ch in password:
        if ch.isupper() != last_case:
            last_case = ch.isupper()
            count_switches += 1

    if count_switches < 1:
        return 1
    elif count_switches < 4:
        return 2
    else:
        return 3


def rate_numeric(password):
    digits = re.compile('\d')
    letters = re.compile('[a-z,A-Z]')
    if bool(digits.search(password)) and bool(letters.search(password)):
        return 1
    else:
        return 0


def rate_length(password):
    if len(password) <=4:
        return 0
    elif len(password) <=10:
        return 1
    else:
        return 2


def rate_special_characters(password):
    symbols = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
    count_symbols = 0
    for ch in password:
        if ch in symbols:
            count_symbols +=1

    if count_symbols <1:
        return 0
    elif count_symbols < 2:
        return 1
    else:
        return 2


if __name__ == '__main__':
    if len(sys.argv) > 1:
        password = sys.argv[1]
        rate = get_password_strength(password)
        prohibited_set = []
        if len(sys.argv) > 2:
            try:
                with open(sys.argv[2]) as data_file:
                    prohibited_set = re.findall(r"[\w']+", data_file.read())
            except UnicodeDecodeError:
                raise Exception("Wrong file type!")
        else:
            raise Exception("Missing prohibited passwords file!")

        check_for_prohibition(password, rate, prohibited_set)
    else:
        raise Exception("Empty password cannot be rated.")

    print("Your password rated as {}".format(rate))

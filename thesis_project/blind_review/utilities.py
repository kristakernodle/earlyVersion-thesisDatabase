import random
import string


def random_string_generator(len_string=10):
    """Generates a random string of length len_string.
    String will contain only lowercase letters and digits.
    :param len_string: length of returned string (default 10)
    :return: string of length len_string
    """

    lowercase_letters_and_digits = list(string.ascii_lowercase + string.digits)
    return ''.join(random.choices(lowercase_letters_and_digits, weights=None, k=len_string))

import datetime
import re


def convert_date_int_yyyymmdd(int_yyyymmdd):
    if isinstance(int_yyyymmdd, datetime.date):
        return int_yyyymmdd
    str_yyyymmdd = str(int_yyyymmdd)
    year = str_yyyymmdd[0:4]
    month = str_yyyymmdd[4:6]
    day = str_yyyymmdd[6:]
    date_tup = tuple(map(int, [year, month, day]))
    return datetime.date(date_tup[0], date_tup[1], date_tup[2])


def decode_genotype(genotype):
    if type(genotype) is str:
        return genotype
    if genotype == 0:
        return 'wild type'
    return 'knock out'


def encode_genotype(genotype):
    if type(genotype) is bool:
        return genotype
    elif genotype == 'wild type':
        return False
    return True


def prep_string_for_db(instring):
    instring_lower = instring.lower()
    split_string = re.split('_|-|/| ', instring_lower)
    joined_string = "_".join(split_string)
    return joined_string





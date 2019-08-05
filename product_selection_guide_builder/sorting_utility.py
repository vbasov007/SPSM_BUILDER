
import re


def parameter_sort_key(string):

    r = re.match(r"^[-]?[\d]+\.?[\d]*", string)

    try:
        res = r.group(0)
        return float(res)
    except AttributeError:
        return 9999999


def is_sortable_as_number(string):

    r = re.match(r"^[-]?[\d]+\.?[\d]*", string)
    try:
        r.group(0)
        return True
    except AttributeError:
        return False


def sorted_smart(lst):
    as_number = [s for s in lst if is_sortable_as_number(s)]
    as_string = [s for s in lst if not is_sortable_as_number(s) and s != '-']

    as_number.sort(key=lambda x: parameter_sort_key(x))
    as_string.sort()

    if '-' in lst:
        as_string += '-'

    return as_number + as_string

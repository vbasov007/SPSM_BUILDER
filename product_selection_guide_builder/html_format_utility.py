import re


def format_multiline_annot(ann_list, max_string_len=50):

    line_break = '<br />'

    res = ''
    cur_str_len = 0
    for ann in ann_list:

        if cur_str_len == 0:
            res += ann
            cur_str_len = len(ann)
        elif cur_str_len + len(ann) + 3 > max_string_len:
            res += line_break + ann
            cur_str_len = len(ann)
        else:
            res += ' | ' + ann
            cur_str_len += len(ann) + 3

    return res


def span_format(css_class, string):
    css_class = css_class.lower()
    css_class = re.sub('<sub>', '_', css_class)
    css_class = re.sub('</sub>', '', css_class)
    css_class = re.sub(' ', '_', css_class)
    return '<span class="{0}">{1}</span>'.format(css_class, string)


def format_val_with_measure_units_html(string):

    #exclude popular housing names
    if string == "62 mm" or string == "34 mm":
        return string

    r = re.match(r"^[-]?[\d]+\.?[\d]*[\s]+", string)

    try:
        val = r.group(0)
    except AttributeError:
        return string

    # exclude long names started with digit
    if len(string[len(val):]) > 7:
        return string

    return '<span class="measure_value">{0}</span><span class="measure_unit">{1}</span>'.format(val, string[len(val):])

import pandas as pd
import re
from sorting_utility import sorted_smart
from html_format_utility import format_val_with_measure_units_html, span_format


def variations(df, col_header):
    a = set(df[col_header].tolist())
    lst = list(a)
    lst = [x if not pd.isna(x) else '-' for x in lst]
    res = list(map(str, lst))

    res = sorted_smart(res)

    return res


def take_only(df, col_name, value):
    return df[df[col_name] == str(value)]


def count_rows(df, col_name, value):
    if col_name in df.columns:
        return take_only(df, col_name, value).shape[0]
    else:
        return 0


def annotations(df, info_col_names):
    data = df[info_col_names]

    out_list = data.values.tolist()
    out = out_list[0]

    out = [re.sub('[ \t]+', ' ', s) for s in out if not pd.isna(s)]

    return out


def annotations_with_title(df, info_col_names):

    data = df[info_col_names]

    out = []
    for col in data:
        val = data[col].values.tolist()[0]
        if val != "-" and val != "":
            val = format_val_with_measure_units_html(val)
            val = span_format(col, val)
            out.append("{0}: {1}".format(col, val))

    return out


def get_single_col_value(df, col_name):
    return df[col_name].values.tolist()[0]

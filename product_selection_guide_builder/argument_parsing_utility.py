
def parse_col_equal_to_list_argument(arg):
    col_name = arg.split('=')[0].strip().strip('"').strip("'")
    val_list = arg.split('=')[1].split(',')
    val_list = [v.strip().strip('"').strip("'") for v in val_list]

    return col_name, val_list


def turn_to_list(arg):
    res = []
    for item in arg:
        try_split = item.split()
        res.extend(try_split)
    return res


def arg_to_header(arg, header_dict, header_list):
    if arg in header_list:
        return arg
    elif arg in header_dict:
        return header_dict[arg]
    else:
        return None


def table_headers_dict(df):
    headers = df.columns.values.tolist()

    out_dict = dict()
    i = 1
    for h in headers:
        out_dict.update({str(i): str(h)})
        i += 1

    return out_dict

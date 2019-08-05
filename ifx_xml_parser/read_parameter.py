import pandas as pd
import re


def read_parameter(df: pd.DataFrame, index, parameter_name, parameter_type='single', first_is_zero=False):
    def split_name_and_number(s: str):
        match = re.match(r"([a-zA-Z0-9_]+[a-zA-Z_]+)([0-9]+)$", s, re.I)
        if match:
            nm, num = match.groups()
            return str(nm), int(num)
        else:
            return '', 0

    if parameter_type == 'single':
        return df.at[index, parameter_name]
    elif parameter_type == 'list':
        res_list = []
        max_res_index = -1
        for col_name in df.columns:
            name, number = split_name_and_number(col_name)
            if name == parameter_name and df.at[index, col_name] != '':
                if int(number) > max_res_index:
                    res_list.extend([''] * (number - max_res_index))
                    max_res_index = number
                res_list[number] = df.at[index, col_name]

        if first_is_zero:
            return res_list
        else:
            return res_list[1:]

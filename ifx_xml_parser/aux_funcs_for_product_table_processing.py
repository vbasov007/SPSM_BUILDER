import re
import pandas as pd
from mylogger import mylog
from error import Error
import datetime


def is_this_valid_data(s: str) -> bool:
    is_not_names = re.match('^[-;, ]+$', s)
    if len(s) == 0 or is_not_names:
        return False
    return True


def take_first_valid_value_in_row(row, source_cols) -> str:
    res = 'no data'
    for v in source_cols:
        if is_this_valid_data(row[v]):
            res = row[v]
    return res


def return_error_if_exception(function):
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except Exception as e:
            return Error(e)
        return Error(None)

    return wrapper


@return_error_if_exception
def fill_column_value(*, df: pd.DataFrame, index, destination_col: str, source_cols: tuple, **options):
    del options
    row = df.loc[index, :]
    df.at[index, destination_col] = take_first_valid_value_in_row(row, source_cols)
    return


@return_error_if_exception
def fill_column_value_all(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del options

    for index, row in df.iterrows():
        df.at[index, destination_col] = take_first_valid_value_in_row(row, source_cols)
    return


@return_error_if_exception
def rename_column(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del options
    df.rename(columns={source_cols[0]: destination_col}, inplace=True)
    return


@return_error_if_exception
def arrange_column_order(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del options
    del destination_col

    columns = df.columns.tolist()

    order_left = [c for c in source_cols if c in columns]

    columns = [c for c in columns if c not in order_left]

    columns.sort()

    new_order = order_left + columns

    for pos, c in enumerate(new_order):
        col = df[c].copy()
        df.drop(c, 1, inplace=True)
        df.insert(pos, c, col)

    return


@return_error_if_exception
def filter_and_remove_empty(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del options

    if destination_col in df.columns:
        df.drop(df[~df[destination_col].isin(source_cols)].index, inplace=True)
    else:
        mylog.warning("Column {0} doesn't exist. Can't filter".format(destination_col))

    df.dropna(axis=1, how='all', inplace=True)

    col_list = list(df.columns)
    for col in col_list:
        if df[col].nunique() == 1 and df[col].tolist()[0] == '':
            df.drop(col, 1, inplace=True)

    mylog.debug("Dropped empty columns. Remaining columns: {0}".format(list(df.columns)))


@return_error_if_exception
def set_parameter_by_ispn(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del options

    ispn = source_cols[0]
    new_value = source_cols[1]

    index = df.index[df['Ispn'] == ispn].tolist()[0]

    if df.at[index, destination_col] != '':
        mylog.warning("Replacing non-blank value at {0} : {1} to {2}".format(ispn,
                                                                             df.at[index, destination_col],
                                                                             new_value))

    df.at[index, destination_col] = new_value


@return_error_if_exception
def set_multiple_parameters_by_ispn(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del options
    try:
        index = df.index[df['Ispn'] == destination_col].tolist()[0]
    except Exception as e:
        mylog.error("Invalid Ispn {0}: {1}".format(destination_col, e))
        return

    for param_name, new_value in zip(*[iter(source_cols)] * 2):
        try:
            if df.at[index, param_name] != '':
                mylog.warning("Replacing non-blank value at {0} : {1} to {2}".format(destination_col,
                                                                                     df.at[index, param_name],
                                                                                     new_value))
            df.at[index, param_name] = new_value
        except Exception as e:
            mylog.error("Invalid Parameter '{0}' in {1}: {2}".format(param_name, destination_col, e))


@return_error_if_exception
def replace_value(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del options

    for old_val, new_val in zip(*[iter(source_cols)] * 2):
        for index, _ in df.iterrows():
            if df.at[index, destination_col] == old_val:
                df.at[index, destination_col] = new_val


@return_error_if_exception
def make_new_product_column(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    def str2date(s):
        if len(s) < 10:
            return None
        try:
            return datetime.datetime.strptime(s[:10], '%Y-%m-%d')
        except ValueError:
            return None

    del destination_col
    del options

    today = datetime.datetime.today()

    df['new_product'] = ''
    for index, _ in df.iterrows():
        new_until = str2date(df.at[index, source_cols[0]])
        if new_until:
            if (new_until - today).days >= 0:
                df.at[index, 'new_product'] = 'new'


@return_error_if_exception
def append_string(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    for index, _ in df.iterrows():
        if len(df.at[index, destination_col]) > 0:
            df.at[index, destination_col] += " " + source_cols[0]


@return_error_if_exception
def max_of_range(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    # get max from range like "1.5..40 V"
    del options
    df[destination_col] = ''
    for index, _ in df.iterrows():
        s = df.at[index, source_cols[0]].split("..")
        if len(s) == 2:
            df.at[index, destination_col] = s[1]
        else:
            df.at[index, destination_col] = s[0]


@return_error_if_exception
def min_of_range(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    # get min from range like "1.5..40 V"
    del options
    for index, _ in df.iterrows():
        s = df.at[index, source_cols[0]].split("..")
        if len(s) == 2:
            min_val = s[0]
            us = s[1].split(" ")
            if len(us) == 2:
                units = us[1]
            else:
                units = ''
            df.at[index, destination_col] = (min_val + " " + units).strip()
        else:
            df.at[index, destination_col] = s[0]


@return_error_if_exception
def fill_empty_values(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del options
    for index, _ in df.iterrows():
        if len(df.at[index, destination_col]) == 0:
            df.at[index, destination_col] = source_cols[0]


@return_error_if_exception
def do_nothing(*, df: pd.DataFrame, destination_col: str, source_cols: tuple, **options):
    del df
    del destination_col
    del source_cols
    del options

import pandas as pd
from error import Error


def selected_products_only(in_df: pd.DataFrame, *,
                           by: str,
                           value_list: list) -> (pd.DataFrame, Error):
    res_df = in_df[in_df[by].isin(value_list)].copy()

    res_df.dropna(axis=1, how='all', inplace=True)

    return res_df, Error(None)


def remove_useless_columns(in_df: pd.DataFrame) -> (pd.DataFrame, Error):
    res_df = in_df.dropna(axis=1, how='all', inplace=False)

    remove_list = []
    for col in res_df:
        if res_df[col].nunique() == 1:
            remove_list.append(col)

    for col in remove_list:
        res_df.drop(col, 1, inplace=True)

    return res_df, Error(None)


def arrange_columns_in_order(in_df: pd.DataFrame,
                             order_left: list) -> (pd.DataFrame, Error):
    columns = list(in_df.columns)

    order_left = [c for c in order_left if c in columns]

    columns = [c for c in columns if c not in order_left]

    columns.sort()

    columns = order_left + columns

    res_df = in_df[columns].copy()

    return res_df, Error(None)

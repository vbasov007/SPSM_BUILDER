from mylogger import mylog
import pandas as pd


def match(first, second):
    # If we reach at the end of both strings, we are done
    if len(first) == 0 and len(second) == 0:
        return True

    # Make sure that the characters after '*' are present
    # in second string. This function assumes that the first
    # string will not contain two consecutive '*'
    if len(first) > 1 and first[0] == '*' and len(second) == 0:
        return False

    # If the first string contains '?', or current characters
    # of both strings match
    if (len(first) > 1 and first[0] == '?') or (len(first) != 0
                                                and len(second) != 0 and first[0] == second[0]):
        return match(first[1:], second[1:]);

        # If there is *, then there are two possibilities
    # a) We consider current character of second string
    # b) We ignore current character of second string.
    if len(first) != 0 and first[0] == '*':
        return match(first[1:], second) or match(first, second[1:])

    return False


def matching(column_series: pd.Series, match_to: str):
    res_val = []
    for index, val in column_series.items():
        res_val.append(match(match_to, val))
    return pd.Series(res_val, index=column_series.index.values.tolist())


def no_matching(column_series: pd.Series, match_to: str):
    res_val = []
    for index, val in column_series.items():
        res_val.append(not match(match_to, val))
    return pd.Series(res_val, index=column_series.index.values.tolist())


def include_only_data(df, col_name, val_list):
    if not val_list:
        mylog.warning('Warning: Empty value list for "{0}"', col_name)
        return

    if col_name in df.columns.values.tolist():
        orig_df = df.copy()

        # df = df.loc[df[col_name] == val_list[0]]
        df = df.loc[matching(df[col_name], val_list[0])]

        for val in val_list[1:]:

            # filtered_df = orig_df.loc[orig_df[col_name] == val]
            filtered_df = orig_df.loc[matching(orig_df[col_name], val)]

            if filtered_df.empty:
                mylog.warning('Warning! Value "{0}" was not found in column "{1}"'.format(val, col_name))
            df = df.append(filtered_df)
    else:
        mylog.error('Error! Column "{0}" is not found in excel columns'.format(col_name))

    return df


def exclude_data(df, col_name, val_list):
    if col_name in df.columns.values.tolist():
        for val in val_list:
            # filtered_df = df.loc[df[col_name] != val]
            filtered_df = df.loc[no_matching(df[col_name], val)]

            if filtered_df.shape == df.shape:
                mylog.warning('Warning! Value "{0}" was not found in column "{1}"'.format(val, col_name))
            df = filtered_df
    else:
        mylog.error('Error! Column "{0}" is not found in excel columns'.format(col_name))

    return df


def include_if_match_string(df, col_name, val_list):
    if col_name in df.columns.values.tolist():
        for s in val_list:
            df = df.loc[df[col_name].str.contains(s)]
    else:
        mylog.error('Error! Column "{0}" is not found in excel columns'.format(col_name))

    return df

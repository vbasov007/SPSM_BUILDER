
def include_only_data(df, col_name, val_list):

    if not val_list:
        print('Warning: Empty value list for "{0}"', col_name)
        return

    if col_name in df.columns.values.tolist():
        orig_df = df.copy()
        df = df.loc[df[col_name] == val_list[0]]
        for val in val_list[1:]:
            filtered_df = orig_df.loc[orig_df[col_name] == val]
            if filtered_df.empty:
                print('Warning! Value "{0}" was not found in column "{1}"'.format(val, col_name))
            else:
                print('Value "{0}" is found {1} times in column "{2}"'.format(val, filtered_df.shape[0], col_name))

            df = df.append(filtered_df)
    else:
        print('Error! Column "{0}" is not found in excel columns'.format(col_name))

    return df


def exclude_data(df, col_name, val_list):

    if col_name in df.columns.values.tolist():
        for val in val_list:
            filtered_df = df.loc[df[col_name] != val]
            if filtered_df.shape == df.shape:
                print('Warning! Value "{0}" was not found in column "{1}"'.format(val, col_name))
            else:
                print('Value "{0}" is found {1} times in column "{2}"'.format(val, filtered_df.shape[0], col_name))
            df = filtered_df
    else:
        print('Error! Column "{0}" is not found in excel columns'.format(col_name))

    return df


def include_if_match_string(df, col_name, string):

    if col_name in df.columns.values.tolist():
        df = df.loc[df[col_name].str.contains(string)]
    else:
        print('Error! Column "{0}" is not found in excel columns'.format(col_name))

    return df

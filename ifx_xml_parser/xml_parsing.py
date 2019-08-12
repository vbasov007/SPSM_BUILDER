from lxml.etree import iterparse
import re
import pandas as pd
from error import Error
from mylogger import mylog


def xml2list(file_name: str, *, progress_indicator=None, estimated_items_count=0) -> (list, Error):
    try:
        # parser = XMLParser(encoding='utf-8', recover=True)
        xml_iter = iterparse(file_name, events=('start', 'end'), recover=True, encoding='utf-8')
    except Exception as e:
        error = Error(e)
        return [], error

    new_item = {}

    item_list = []
    count = 0
    for event, elem in xml_iter:
        if event == 'start' and elem.tag == 'item':
            new_item = {}
        elif event == 'end' and elem.tag == 'item':
            item_list.append(new_item)
            elem.clear()
            if progress_indicator:
                progress_indicator(count, estimated_items_count)
                count += 1
        elif event == 'end' and elem.tag != 'item':
            # remove multiple spaces and store
            tag = re.sub(r"\s\s+", " ", str(elem.tag))
            text = re.sub(r"\s\s+", " ", str(elem.text))
            new_item.update({tag: text})

    return item_list, Error(None)


def ispn_xml_parameters_to_str(param: dict) -> str:
    if param['DataType'] == 'TEXT':
        return param['ValueChar']

    for k in param:
        param[k] = param[k].rstrip('0').rstrip('.') if '.' in param[k] else param[k]

    if param['RangeDefinition'] == 'true':
        return "{0}..{1} {2}".format(param['ValueMin'],
                                     param['ValueMax'],
                                     param['Unit'])
    return "{0}{1}{2} {3}".format(param['ValueNumeric'],
                                  param['ValueMin'],
                                  param['ValueMax'],
                                  param['Unit'])


def document_ref_to_str(param: dict) -> str:
    return param['DownloadUrl']


def xml2excel_params(input_file_name: str,
                     *,
                     row_key: str,
                     column_key: str,
                     column_modifier_key=None,
                     convert2str_method,
                     is_filter_pass=None,
                     progress_indicator=None,
                     estimated_items_count=0) -> (pd.DataFrame, Error):
    mylog.info("Reading {0}...".format(input_file_name))
    item_list, error = xml2list(input_file_name,
                                progress_indicator=progress_indicator,
                                estimated_items_count=estimated_items_count)
    if error:
        return None, Error(str(error) + "File: {0}".format(input_file_name))

    print('\n')
    mylog.info("Processing {0}...".format(input_file_name))
    parts_database = {}
    count = 0
    total_item_count = len(item_list)
    for item in item_list:

        if is_filter_pass:
            if not is_filter_pass(item):
                continue

        for k in item:
            item[k] = '' if item[k] == 'None' else item[k]

        part_number = item[row_key]
        parameter_name = item[column_key]
        param_str = convert2str_method(item)

        # mylog.debug("{0} {1} {2}".format(part_number, parameter_name, param_str))
        if progress_indicator:
            progress_indicator(count, total_item_count, "{0} {1}".format(part_number, parameter_name))
            count += 1

        if part_number not in parts_database:
            parts_database.update({part_number: {row_key: part_number}})

        if column_modifier_key:
            if len(item[column_modifier_key]) > 0:
                parameter_name = "{0} {1}".format(parameter_name, item[column_modifier_key])

        if parameter_name not in parts_database[part_number]:
            parts_database[part_number].update({parameter_name: param_str})
        else:
            if param_str not in parts_database[part_number][parameter_name]:
                parts_database[part_number][parameter_name] += "; {0}".format(param_str)

    df = pd.DataFrame.from_dict(parts_database, orient='index')

    return df, Error(None)


def xml2excel_merge_partnums(input_file_name: str,
                             item_key,
                             *,
                             progress_indicator=None,
                             estimated_items_count=0) -> (pd.DataFrame, Error):
    mylog.info("Reading {0}...".format(input_file_name))
    item_list, error = xml2list(input_file_name,
                                progress_indicator=progress_indicator,
                                estimated_items_count=estimated_items_count)
    if error:
        return None, Error(str(error) + "File: {0}".format(input_file_name))

    print('\n')
    mylog.info("Processing {0}...".format(input_file_name))

    parts_database = {}
    total_item_count = len(item_list)
    count = 0
    for item in item_list:
        part_number = item[item_key]
        if progress_indicator:
            progress_indicator(count, total_item_count, part_number)
            count += 1

        if part_number not in parts_database:
            parts_database.update({part_number: {}})

        for tag in item:
            current = parts_database[part_number].get(tag, [])

            new = item[tag]

            if new != 'None' and new != '':
                if new not in current:
                    new_val = current + [new]
                else:
                    new_val = current
            else:
                new_val = current
            parts_database[part_number].update({tag: new_val})

    print('\n')

    df = pd.DataFrame.from_dict(parts_database, orient='index')

    def list2str(val):
        if isinstance(val, list):
            return "; ".join(val)
        else:
            return str(val)

    df = df.applymap(list2str)

    return df, Error(None)


def xml2excel_all_lines(input_file_name: str) -> (pd.DataFrame, Error):
    item_list, error = xml2list(input_file_name)
    if error:
        return None, Error(str(error) + "File: {0}".format(input_file_name))

    parts_database = {}
    for count, item in enumerate(item_list):
        print(item)
        parts_database.update({count: {}})

        for tag in item:
            parts_database[count].update({tag: item[tag]})

    df = pd.DataFrame.from_dict(parts_database, orient='index')

    return df, Error(None)


def xml2dict(input_file_name: str,
             key_tag_name: str,
             value_tag_name: str,
             *,
             progress_indicator=None,
             estimated_items_count=0) -> (dict, Error):
    mylog.info("Reading file {0}...".format(input_file_name))
    item_list, error = xml2list(input_file_name,
                                progress_indicator=progress_indicator,
                                estimated_items_count=estimated_items_count)
    if error:
        return None, Error(str(error) + "File: {0}".format(input_file_name))

    print('\n')
    mylog.info("Building dictionary...".format(input_file_name))

    res = {}
    count = 0
    total_item_count = len(item_list)
    for item in item_list:

        if progress_indicator:
            progress_indicator(count, total_item_count)
            count += 1

        if (key_tag_name in item) and (value_tag_name in item):
            res.update({item[key_tag_name]: item[value_tag_name]})
        else:
            mylog.warning("No tag-value match!")

    return res, Error(None)


def get_number_of_items(input_file_name: str) -> (int, Error):
    try:
        xml_iter = iterparse(input_file_name, events=('start', 'end'), recover=True)
    except Exception as e:
        error = Error(e)
        return 0, error

    count = 0
    for event, elem in xml_iter:
        if event == 'end' and elem.tag == 'item':
            count += 1
            elem.clear()

    return count, Error(None)

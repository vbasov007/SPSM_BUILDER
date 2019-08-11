from collections import OrderedDict
from excel import read_excel
from read_parameter import read_parameter
import aux_funcs_for_product_table_processing
from error import Error
from mylogger import mylog


class ProductTableBuilder:

    def __init__(self):
        self.steps = OrderedDict()
        self.selected_values = tuple()
        self.select_by = ''
        self.columns_in_order = []

    def add_step(self, *, step_name: str, destination_col: str = '', source_cols: tuple = (), proc, **options):
        if step_name in self.steps:
            raise Exception('Step {0} already exist'.format(step_name))

        self.steps[step_name] = {'destination_col': destination_col,
                                 'source_cols': source_cols,
                                 'options': options,
                                 'proc': proc}

    def set_product_filter(self, selected_values: tuple, select_by: str):
        self.selected_values = selected_values
        self.select_by = select_by

    def set_column_order(self, *columns_in_order):
        self.columns_in_order = columns_in_order

    def _do_single_step(self, name, df):

        proc = self.steps[name]['proc']
        proc(df=df,
             destination_col=self.steps[name]['destination_col'],
             source_cols=self.steps[name]['source_cols'],
             options=self.steps[name]['options'])

    def do_all_steps(self, df):
        for name in self.steps:
            mylog.info("Step {0}".format(name))
            self._do_single_step(name, df)

    def init_from_file(self, xlsx_file_path: str, sheet_name: str) -> Error:

        mylog.info('Reading steps from file {0}'.format(xlsx_file_path))
        df, error = read_excel(xlsx_file_path, sheet_name=sheet_name, replace_nan='')

        if error:
            return error

        try:
            for index, _ in df.iterrows():
                mylog.info('Adding step {0}'.format(read_parameter(df, index, 'step_name')))
                self.add_step(step_name=read_parameter(df, index, 'step_name'),
                              destination_col=read_parameter(df, index, 'destination'),
                              source_cols=read_parameter(df, index, 'source', parameter_type='list'),
                              proc=getattr(aux_funcs_for_product_table_processing, read_parameter(df, index, 'func')))
        except Exception as e:
            return Error(e)

        return Error(None)

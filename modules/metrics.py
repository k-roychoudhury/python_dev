r"""This module contains functions that store program metrics

The jobs that are intended to be performed by this moule are purely secondary
in nature. As such even if these jobs raise exceptions or fail directly, these
must not interfere with the main script / program being run.

To address this problem, the module will manage its own resources in a
different thread that will be started on import of this module and will be
closed when the calling program terminates.

The module is not intened to be executed as-is, but, in the event that it is,
it will display it's own details."""

# importing standard modules --------------------------------------------------
import os
import sys
import datetime
import atexit
from collections import OrderedDict


# importing third party modules -----------------------------------------------
import pandas


# class definitions -----------------------------------------------------------
class Metrics:
    """This class is meant to be initialized with a list of metric names that
    need to be captured during the execution of the program. An instance of
    this class will provide the neccessary attributes as described by the list.

    Further more, this class' api will be used for all saving purposes"""
    

    def __init__(self):
        self.__metrics__ = OrderedDict()
        return


    def __repr__(self) -> str:
        repr: str = "Metrics({})".format(self.__metrics__)
        return repr # end of __repr__


    def __str__(self) -> str:
        metrics_string: str = ""
        for key in self.__metrics__.keys():
            metrics_string += "'{}':'{}',".format(key, self.__metrics__[key])
        metrics_string = metrics_string[0:-1]
        string: str = "Metrics({})".format(metrics_string)
        return string


    def save(self, metric_name: str, metric_value) -> None:
        """This function adds another metric with name 'metric_name' and saves
        it with the value 'metric_value'"""
        self.__metrics__.__setitem__(metric_name, metric_value)
        return


    def keys(self) -> tuple:
        """Returns a tuple containing all keys in __metrics__"""
        return tuple(self.__metrics__.keys())


    def values(self) -> tuple:
        """Returns a tuple containing all values in __metrics__"""
        return tuple(self.__metrics__.values())


    pass # end of Metrics definition


# module global variables -----------------------------------------------------
__DEBUG__: bool = True
    # Debug boolean to switch modes

CALLING_SCRIPT_ABSOLUTE_PATH: str = None
    # this is initialized on import

CALLING_SCRIPT_NAME: str = None
    # this is initialized on import

PROGRAM_METRICS_TABLE: pandas.DataFrame = None
    # this is initialized on import; provided a valid metrics file with the name
    # of the calling script / program is available at the location. Else it 
    # will remain None untill first initialization.

GLOBAL_METRICS_OBJECT: Metrics = Metrics()
    # this is used by the front api of the module; (functions in section 'main
    # api functions')

CALLING_SCRIPT_METRICS_FILE_NAME: str = None
    # this is initialized on import

CALLING_SCRIPT_BACKUP_METRICS_FILE_NAME: str = None
    # this is initialized on import

# module parameters (basic config) --------------------------------------------
EXCEL_FILE_SHEET_NAME: str = 'metrics_data'
    # this is the default sheet value upon initialization


# module background(private) functions ----------------------------------------
def __debug_print__(*args) -> None:
    """Prints to Std. Out. Module specific function to be used privately"""
    if __DEBUG__ is True:
        print("metrics_debug_print:", end=' ')
        for item in args:
            print(item, end=' ')
        print(end='\n')
    return


def __write_to_file__(
    dataframe: pandas.DataFrame, 
    sheet_name: str, 
    full_file_path: str,
    file_mode: str = "w"
    ) -> None:
    # pylint: disable=abstract-class-instantiated
    with pandas.ExcelWriter(
        full_file_path, 
        engine='xlsxwriter',
        mode = file_mode
        ) as writer:
        dataframe.to_excel(
            writer, 
            sheet_name=sheet_name,
            index=False
        )
        worksheet = writer.sheets[sheet_name]  
        # pull worksheet object
        for idx, col in enumerate(dataframe): 
            # loop through all columns
            series = dataframe[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
            )) + 1  # adding a little extra space
            worksheet.set_column(idx, idx, max_len)  # set column width
    return


def __on_exit__() -> None:
    """This function contains clean-up code for the module. Most notable is
    writing the GLOBAL_METRICS_OBJECT to the excel file"""
    __debug_print__("Called __on_exit__")
    dump()
    return # end of __on_exit__


# initialization functions ----------------------------------------------------
def basic_config(
    workbook_sheet_name: str = None,
    metrics_headers: list = None
    ):
    """This function takes arguments to customize the behaviour of the metrics
    module. MORE TO FOLLOW"""
    global EXCEL_FILE_SHEET_NAME
    EXCEL_FILE_SHEET_NAME = workbook_sheet_name \
        if workbook_sheet_name is not None else 'metrics_data'

    global GLOBAL_METRICS_OBJECT
    if type(metrics_headers) == list:
        for header in metrics_headers:
            GLOBAL_METRICS_OBJECT.save(header, None)

    pass


# main api functions ----------------------------------------------------------
def save(metric_name: str, metric_value) -> None:
    """This function takes a 'metric_name' to be saved with corresponding value
    'metric_value'. It is expected that 'metric_value' will be a atomic data 
    type (not list or dict or set or something similar)"""
    if type(metric_value) in [list, dict, set]:
        raise ValueError("metric_value must not be a container object")

    global GLOBAL_METRICS_OBJECT

    GLOBAL_METRICS_OBJECT.save(metric_name, metric_value)
    return # end of metrics.save


def dump() -> None:
    """This function writes the GLOBAL_METRICS_OBJECT to the metrics excel file
    of the calling program. Automatically called at program exit."""
    __debug_print__("Called dump")

    global GLOBAL_METRICS_OBJECT
    global PROGRAM_METRICS_TABLE
    global EXCEL_FILE_SHEET_NAME
    
    if PROGRAM_METRICS_TABLE is None:
        # a new pandas.DataFrame object must be created and input with a single
        # row of data (GLOBAL_METRICS_OBJECT). The table headers are the key's 
        # in the GLOBAL_METRICS_OBJECT.
        PROGRAM_METRICS_TABLE = pandas.DataFrame(
            data=[GLOBAL_METRICS_OBJECT.values()],
            columns=GLOBAL_METRICS_OBJECT.keys()
        )
        __debug_print__("New Metrics Table\n", PROGRAM_METRICS_TABLE)

        full_file_path: str = os.path.join(
            CALLING_SCRIPT_ABSOLUTE_PATH, CALLING_SCRIPT_METRICS_FILE_NAME
        )
        __write_to_file__(
            PROGRAM_METRICS_TABLE, EXCEL_FILE_SHEET_NAME, full_file_path
        )

        pass
    else:
        # Check for table header sync with keys in GLOBAL_METRICS_OBJECT
        __debug_print__("Existing Metrics Table\n", PROGRAM_METRICS_TABLE)

        # There are two cases to explore:
        # 1) A complete match between the keys in GLOBAL_METRICS_OBJECT and the
        # headers of PROGRAM_METRICS_TABLE.
        # 2) A mismatch between the two.
        header_match: bool = True
        E_headers = set(PROGRAM_METRICS_TABLE.keys())
        G_headers = set(GLOBAL_METRICS_OBJECT.keys())
        if len(E_headers) == len(G_headers):
            if len(E_headers - G_headers) != 0:
                header_match = False
        else:
            header_match = False

        if header_match:
            __debug_print__("Existing & Current headers match")
            PROGRAM_METRICS_TABLE = PROGRAM_METRICS_TABLE.append(
                GLOBAL_METRICS_OBJECT.__metrics__,
                ignore_index=True
            )
            __debug_print__("New Metrics Table\n", PROGRAM_METRICS_TABLE)

            full_file_path: str = os.path.join(
                CALLING_SCRIPT_ABSOLUTE_PATH, CALLING_SCRIPT_METRICS_FILE_NAME
            )
            __write_to_file__(
                PROGRAM_METRICS_TABLE, EXCEL_FILE_SHEET_NAME, full_file_path
            )
            pass
        else:
            __debug_print__("Existing & Current headers do not match")
            # A decision needs to be made: whether to discard the previous
            # metrics or to compute some amalgamation of the previous one and
            # the new one

            # OR - rename the previous file to 'some backup' and create a new
            # file for the new metrics
            full_file_path: str = os.path.join(
                CALLING_SCRIPT_ABSOLUTE_PATH, 
                CALLING_SCRIPT_BACKUP_METRICS_FILE_NAME
            )
            # 1) Search for the default backup file
            if os.path.isfile(full_file_path):
                __debug_print__("Backup Metrics file exists")
                # get list of sheets, add a new sheet for the old metrics
                excel_file = pandas.ExcelFile(full_file_path)

                backup_sheet_names = list(excel_file.sheet_names)
                backup_dataframes = [excel_file.parse(sheet_name=sheet)
                    for sheet in excel_file.sheet_names]
                
                
                # Take the last entry of the list: excel_file.sheet_names and
                # get the last number.
                sheet_name: str = "back_up_sheet_{}_{:02d}"
                sheet_number: int = 1
                current_date = datetime.datetime.today().strftime('%Y_%b_%d')
                if current_date == \
                    "_".join(excel_file.sheet_names[-1].split('_')[-4: -1]):
                    sheet_number: int \
                        = int(excel_file.sheet_names[-1].split('_')[-1])
                    sheet_number += 1
                sheet_name = \
                    sheet_name.format(str(current_date), sheet_number)

                backup_dataframes.append(PROGRAM_METRICS_TABLE)
                backup_sheet_names.append(sheet_name)

                # write all backup_dataframes to file
                # pylint: disable=abstract-class-instantiated
                with pandas.ExcelWriter(
                    full_file_path, engine='xlsxwriter') as writer:
                    for dataframe, sheet_name \
                        in zip(backup_dataframes, backup_sheet_names):

                        dataframe.to_excel(
                            writer, sheet_name=sheet_name, index=False
                        )
                        # pull worksheet object
                        worksheet = writer.sheets[sheet_name]  
                    
                        for idx, col in enumerate(dataframe): 
                            # loop through all columns
                            series = dataframe[col]
                            max_len = max((
                                series.astype(str).map(len).max(),  
                                # len of largest item
                                len(str(series.name))  
                                # len of column name/header
                            )) + 1  # adding a little extra space
                            worksheet.set_column(idx, idx, max_len)  
                            # set column width
                        
                pass
            else:
                __debug_print__("Backup Metrics file does not exist")
                # write a new sheet with old metrics
                current_date = datetime.datetime.today().strftime('%Y_%b_%d')
                sheet_name: str = "back_up_sheet_" + str(current_date) + "_01"
                __write_to_file__(
                    PROGRAM_METRICS_TABLE, sheet_name, full_file_path
                )

                pass
            
            # write the new metrics 
            PROGRAM_METRICS_TABLE = pandas.DataFrame(
                data=[GLOBAL_METRICS_OBJECT.values()],
                columns=GLOBAL_METRICS_OBJECT.keys()
            )
            __debug_print__("New Metrics Table\n", PROGRAM_METRICS_TABLE)

            full_file_path: str = os.path.join(
                CALLING_SCRIPT_ABSOLUTE_PATH, CALLING_SCRIPT_METRICS_FILE_NAME
            )
            __write_to_file__(
                PROGRAM_METRICS_TABLE, EXCEL_FILE_SHEET_NAME, full_file_path
            )
            pass

        pass
    
    return


# on import as main -----------------------------------------------------------
if __name__ == "__main__":
    print(__doc__)
    print("\nMuch like it is doing right now!")
else:
    # This block is executed if the module is imported by another module
    # or script.
    __debug_print__("Metrics imported as a Module!")


    # Register the __on_exit__ function of the module with atexit so that it is
    # called when the main program exits
    atexit.register(__on_exit__)


    # The main objective is to find out which script or program imported this
    # module, although it is expected that it will be imported at the top-most
    # level (main script) of the program.
    rel_path_to_file, _ = os.path.split(sys.argv[0])
    CALLING_SCRIPT_ABSOLUTE_PATH = os.path.join(os.getcwd(), rel_path_to_file)
    __debug_print__(
        "Calling script absolute path:", CALLING_SCRIPT_ABSOLUTE_PATH
    )


    # Second objective is to find out the name of the script or program which
    # imported this module. This will be used as the base for the excel file
    # written by pandas for the metrics.
    # find out the name of the calling code
    _, program_name = os.path.split(sys.argv[0])
    CALLING_SCRIPT_NAME = program_name.split('.')[0] + "_metrics"
    __debug_print__("Calling script name:", program_name)


    # Once the name has been generated, check for the file CALLING_SCRIPT_NAME
    # with '.xlsx' extension at CALLING_SCRIPT_ABSOLUTE_PATH. If such a file is
    # not found at the location, generate a new file during the run of the
    # program. Else, read the excel file and load the metrics from it.
    CALLING_SCRIPT_METRICS_FILE_NAME = CALLING_SCRIPT_NAME + ".xlsx"
    CALLING_SCRIPT_BACKUP_METRICS_FILE_NAME \
        = CALLING_SCRIPT_NAME + "_backup.xlsx"
    full_file_path: str = os.path.join(
        CALLING_SCRIPT_ABSOLUTE_PATH, CALLING_SCRIPT_METRICS_FILE_NAME
    )
    if os.path.isfile(full_file_path) is True:
        # Read the excel file and load the pandas dataframe
        __debug_print__("Metrics file found for '{}': {}". \
            format(program_name, CALLING_SCRIPT_METRICS_FILE_NAME))
        
        __debug_print__("Metrics file path: {}".format(full_file_path))
        PROGRAM_METRICS_TABLE = pandas.read_excel(
            full_file_path,
            sheet_name=EXCEL_FILE_SHEET_NAME,
        )

        __debug_print__(
            "Existing Metrics Table - On Import\n", 
            PROGRAM_METRICS_TABLE
        )

        pass
    else:
        # First initialization must be done by the program.
        __debug_print__("Metrics file '{}' not found for '{}'". \
            format(CALLING_SCRIPT_METRICS_FILE_NAME, program_name))
        
        # Set the PROGRAM_METRICS_TABLE to None just to be sure
        PROGRAM_METRICS_TABLE = None

        pass

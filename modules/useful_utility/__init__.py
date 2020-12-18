r"""This module contains usefull utility functions for variety of tasks.

Example definition of a debug print function:
DEBUG: bool = True # define this at the top of the script
def debug_print(*args) -> None:
    "Prints to Std. Out. Module specific function to be used privately"
    if DEBUG is True:
        print("<some identification>", end=' ')
        for item in args:
            print(item, end=' ')
        print(end='\n')
    return
    
    """

# importing standard modules --------------------------------------------------
import logging

# importing third party modules -----------------------------------------------
import pandas

# Function Definitions --------------------------------------------------------
def write_excel_file(
    dataframe: pandas.DataFrame, 
    sheet_name: str, 
    full_file_path: str,
    file_mode: str = "w"
    ) -> None:
    r"""Uses the pandas.ExcelWriter to write an excel file with given filename
    and sheet name. Beautifies the file with width adjusted columns."""
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
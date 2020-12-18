r"""Main program to explore and test the logging modules different available 
features."""

r"""Need to answer some questions:- 
Why is logging needed? - To know which parts of code have executed and to have
records of all events occurring during the execution of the logged code.

What are my requirements of logging? (will change in the future, no dobut) -
1) Simple logging events to file.
2) Configuring the format for log records.
3) How to configure logging for modules developed by me. How to enable or
disable them as per requirement.
4) Log File rotation, at all kinds of periods, preferably daily.
5) Customizing log file directory location
"""

# importing standard modules --------------------------------------------------
import logging
import logging.handlers
import os

r"""This is how you import the logging module. ;P There are two ways of
initializing / configuring the module.
    1) By using the 'logging.basicConfig()' function.
    2) By using a configuration file"""

r"""Answer 1 - Logging module provides the methodes 'info', 'error', 'warning'
and 'critical' to log events to file"""

def function1() -> None:
    r"""Demonstrates simple logging functions"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(lineno)d %(name)-12s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M'
    )
    logging.info("In Function1, after call to logging.basicConfig")
    logging.warning("A simple warning event log")
    logging.error("A simple error event log")
    logging.critical("A simple critical event log")
    try:
        raise Exception("Sample error!")
    except Exception as e:
        logging.exception(e)
        pass
    return
    

def function2() -> None:
    r"""Demonstrates use of format strings and formater objects"""
    # logging.basicConfig(
    #     level=logging.DEBUG,
    #     datefmt='%m-%d %H:%M'
    # )
    logger = logging.getLogger('function2')
    formatter = logging.Formatter(
        '%(asctime)s %(lineno)d - %(name)-12s - %(levelname)-8s - %(message)s')
    ch = logging.StreamHandler()
    #ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("In Function2")
    logger.warning("A simple warning event log")
    logger.error("A simple error event log")
    logger.critical("A simple critical event log")
    return


def function3() -> None:
    r"""Log file rotation
    Value       Type of interval                                                    If/how atTime is used
    'S'         Seconds                                                             Ignored
    'M'         Minutes                                                             Ignored
    'H'         Hours                                                               Ignored
    'D'         Days                                                                Ignored
    'W0'-'W6'   Weekday (0=Monday)                                                  Used to compute initial rollover time
    'midnight'  Roll over at midnight, if atTime not specified, else at time atTime Used to compute initial rollover time
    """
    filename: str = os.path.join("logs", "temp.txt")
    formatter = logging.Formatter(
        '%(asctime)s %(lineno)d - %(name)-12s - %(levelname)-8s - %(message)s')
    trf = logging.handlers.TimedRotatingFileHandler(filename, when='midnight', interval=1)
    logger = logging.getLogger('function3')
    trf.setFormatter(formatter)
    logger.addHandler(trf)
    logger.info("In Function3")
    logger.warning("A simple warning event log")
    logger.error("A simple error event log")
    logger.critical("A simple critical event log")
    return


if __name__ == "__main__":
    print(__doc__)
    # function1()
    # function2()
    function3()
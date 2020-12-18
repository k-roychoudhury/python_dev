import logging
import datetime

from logging_aid import logging_utils
import metrics_aid.metrics as metrics


if __name__ == "__main__":
    metrics.basic_config(
        metrics_headers=["Execution Start Timestamp", "Temporary Metric 1", 
        "Execution End Timestamp", "Temporary Metric 2", "Temporary Metric 3"]
    )

    metrics.save(
        "Execution Start Timestamp", 
        datetime.datetime.now().strftime("%d-%b-%Y::%H:%M:%S:%f")
    )

    logging.basicConfig(
        level=logging.DEBUG,
        filename=logging_utils.get_log_file_name(log_directory_path="logs"),
        filemode="a"
    )

    metrics.save(
        "Temporary Metric 1", 
        "Kunal"
    )

    metrics.save(
        "Temporary Metric 2", 
        "Roy"
    )

    logger = logging.getLogger()
    print("Hello World!")
    logger.debug("Hello World!")

    
    metrics.save(
        "Execution End Timestamp", 
        datetime.datetime.now().strftime("%d-%b-%Y::%H:%M:%S:%f")
    )

    print(metrics.GLOBAL_METRICS_OBJECT)
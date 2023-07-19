import logging
import os


def logManager():

    # define the path to the log file
    log_dir = "logs"
    log_file_path = os.path.join(log_dir, "logs.log")

    # create the log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(process)d - %(message)s")



    # create a file handler and set the formatter
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
import logging
import os

def setup_logging(log_dir="logs"):
    # Create the log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Configure logging for each module using __name__
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Avoid adding handlers if the logger already has them
        if not logger.handlers:
            # Define the log file path using the module name
            log_file = os.path.join(log_dir, f"{name}.log")
            formatter = logging.Formatter("[%(asctime)s][FILE:%(name)s][%(levelname)s]-[%(message)s ]")

            # Add FileHandler to write logs to a file
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    return get_logger
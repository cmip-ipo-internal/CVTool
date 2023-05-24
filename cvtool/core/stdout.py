import logging

# Configure logger
def log(name, level = 'warning'):

    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))

    # Create a formatter and add it to the console handler
    formatter = logging.Formatter(name+':%(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(console_handler)

    return logger




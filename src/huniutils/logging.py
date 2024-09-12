import os


def generate_plain_logger(
    main_dir: str,
    logger_name: str
    ) -> dict:
    r"""generate plain logger configuration
    
    Parmeters
    ---------
    main_dir: str
        main project directory where log files will be collected
    logger_name: str
        name of logg file

    Notes
    -----
    - useful explanation
        - https://stackoverflow.com/questions/57451246/how-to-set-up-multiple-loggers-with-different-settings-using-logging-config-dict
    """
    if not os.path.isdir(main_dir):
        raise OSError('invalid input, input directory not found')
    
    if not isinstance(logger_name, str):
        raise TypeError('invalid input, logger_name should be string')

    if not os.path.isdir(os.path.join(main_dir, 'log')):
        os.mkdir(
            os.path.join(main_dir, 'log')
        )
        # print('`log` folder is created')
    
    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format" : "%(asctime)s %(levelname)s:%(message)s"}
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "formatter": "simple",
                "level": "DEBUG",
                "filename": os.path.join(main_dir, "log", f"{logger_name}.log")
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": "ERROR"
            }
        },
        'loggers': {
            logger_name: {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True  
            },
        }
    }
    return logger_config

def generate_class_logger(
    main_dir: str,
    class_name: str
    ) -> dict:
    """generate class logger configuration with class Name
    
    Parameters
    ----------
    main_dir: str
        main project directory where log files will be collected
    class_name: str
        name of class
    """
    if not os.path.isdir(main_dir):
        raise OSError('invalid input, input directory not found')
    
    if not isinstance(class_name, str):
        raise TypeError('invalid input, class_name should be string')
    
    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format" : "%(asctime)s %(levelname)s:%(message)s"}
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "formatter": "simple",
                "level": "DEBUG",
                "filename": os.path.join(main_dir, "log", f"{class_name}.log")
            },
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "level": "ERROR"
            }
        },
        'loggers': {
            class_name: {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True  
            },
        }
    }
    return logger_config


if __name__ == "__main__":
    import logging
    from logging.config import dictConfig

    # test: generate_plain_logger
    dictConfig(generate_plain_logger('log_test'))
    logger = logging.getLogger(__name__)
    logger.debug('debug code')
    logger.info('info code')
    logger.warning('warn code')
    del logger
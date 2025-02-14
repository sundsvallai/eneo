import logging
import sys

from intric.main.config import get_loglevel

# Disable loggers from other packages if loglevel is INFO or above
for _logger in logging.root.manager.loggerDict:
    if get_loglevel() <= logging.DEBUG:
        logging.getLogger(_logger).setLevel(logging.INFO)
    else:
        logging.getLogger(_logger).setLevel(logging.CRITICAL)


# noqa Copied from https://dev.to/taikedz/simple-python-logging-and-a-digression-on-dependencies-trust-and-copypasting-code-229o
class SimpleLogger(logging.Logger):
    FORMAT_STRING = '%(asctime)s | %(levelname)s | %(name)s : %(message)s'
    ERROR = logging.ERROR
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG

    def __init__(
        self,
        name="main",
        fmt_string=FORMAT_STRING,
        level=logging.WARNING,
        console=True,
        files=None,
    ):
        logging.Logger.__init__(self, name, level)
        formatter_obj = logging.Formatter(fmt_string)

        if files is None:
            files = []
        elif isinstance(files, str):
            files = [files]

        def _add_stream(handler: logging.Handler, **kwargs):
            handler = handler(**kwargs)
            handler.setLevel(level)
            handler.setFormatter(formatter_obj)
            self.addHandler(handler)

        if console is True:
            _add_stream(logging.StreamHandler, stream=sys.stdout)

        for filepath in files:
            _add_stream(logging.FileHandler, filename=filepath)


def get_logger(module_name: str):
    # If we don't add a handler manually one will be created for us
    return SimpleLogger(name=module_name, level=get_loglevel())

import logging

from prompt_toolkit import print_formatted_text
from prompt_toolkit.application import create_app_session_from_tty
from prompt_toolkit.formatted_text import FormattedText


class TtyLogHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            color = "ansired"
        elif record.levelno == logging.WARNING:
            color = "ansiyellow"
        else:
            color = "ansywhite"
        log_entry = self.format(record)
        formatted_log_entry = FormattedText([(color, f"\n{log_entry}")])
        with create_app_session_from_tty():
            print_formatted_text(formatted_log_entry)
